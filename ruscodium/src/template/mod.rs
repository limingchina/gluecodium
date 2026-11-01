//! A bounded Trimou-compatible renderer for explicit reference snapshots.
mod graph;
pub mod native_controls;
pub mod native_cpp;
mod parser;
pub use graph::Graph;
use parser::{expression, Expression};
pub use parser::{parse, Node};
use serde_json::{json, Map, Value};
use std::{
    collections::BTreeMap,
    fs,
    path::{Component, Path, PathBuf},
};

const MAX_OUTPUT: usize = 16 * 1024 * 1024;
const MAX_DEPTH: usize = 128;

/// Render a version 1 render-request. The returned bytes are complete before any output is written.
pub fn render(root: impl AsRef<Path>, request: &Value) -> Result<String, String> {
    if request.get("schema").and_then(Value::as_str) != Some("gluecodium.template.render-request")
        || request.get("version").and_then(Value::as_u64) != Some(1)
    {
        return Err("unsupported render request schema or version".into());
    }
    let graph = Graph::import_with_absences(
        request.get("snapshot"),
        request.get("property_overlays"),
        request.get("absent_properties"),
    )?;
    let data = request
        .get("data")
        .ok_or("render request has no data")?
        .clone();
    graph.validate(&data)?;
    let hooks = request.get("hooks").cloned().unwrap_or_else(|| json!({}));
    validate_hooks(&graph, &hooks)?;
    let native_cpp = request
        .get("native_cpp")
        .map(native_cpp::NativeCppConfig::parse)
        .transpose()?;
    if native_cpp.is_some()
        && hooks
            .get("names")
            .and_then(Value::as_array)
            .is_some_and(|v| !v.is_empty())
    {
        return Err("native_cpp cannot be combined with name hooks".into());
    }
    let native_predicates = native_cpp.as_ref().is_some_and(|c| c.predicates);
    let native_sorters = native_cpp.as_ref().is_some_and(|c| c.sorters);
    for (enabled, category) in [
        (native_predicates, "predicates"),
        (native_predicates, "registered_predicates"),
        (native_sorters, "sorters"),
    ] {
        if enabled
            && hooks
                .get(category)
                .and_then(Value::as_array)
                .is_some_and(|v| !v.is_empty())
        {
            return Err(format!(
                "native_cpp cannot be combined with {category} hooks"
            ));
        }
    }
    let native_cpp = native_cpp
        .map(|config| native_cpp::NativeCppResolver::new(&graph, config))
        .transpose()?;
    let root = fs::canonicalize(root.as_ref()).map_err(|e| format!("template root: {e}"))?;
    if !root.is_dir() {
        return Err("template root is not a directory".into());
    }
    let name = request
        .get("template")
        .and_then(Value::as_str)
        .ok_or("render request has no template name")?;
    let mut engine = Engine {
        root,
        graph,
        hooks,
        native_cpp,
        native_predicates,
        native_sorters,
        definitions: BTreeMap::new(),
        frames: vec![Frame {
            value: data,
            locals: Map::new(),
        }],
        depth: 0,
        switches: Vec::new(),
    };
    engine.partial(name)
}
fn validate_hooks(graph: &Graph, hooks: &Value) -> Result<(), String> {
    let object = hooks.as_object().ok_or("hooks must be an object")?;
    for category in object.keys() {
        if !["names", "predicates", "sorters", "registered_predicates"].contains(&category.as_str())
        {
            return Err(format!("unsupported hook category {category}"));
        }
    }
    if let Some(names) = object.get("registered_predicates") {
        let mut seen = std::collections::BTreeSet::new();
        for name in names
            .as_array()
            .ok_or("hooks.registered_predicates must be an array")?
        {
            let name = name
                .as_str()
                .filter(|s| !s.is_empty())
                .ok_or("invalid registered predicate name")?;
            if !seen.insert(name) {
                return Err(format!("duplicate registered predicate {name}"));
            }
        }
    }
    for category in ["names", "predicates", "sorters"] {
        let mut seen = BTreeMap::new();
        if let Some(values) = object.get(category) {
            for entry in values
                .as_array()
                .ok_or_else(|| format!("hooks.{category} must be an array"))?
            {
                graph.validate(entry)?;
                let e = entry
                    .as_object()
                    .ok_or_else(|| format!("hooks.{category} entry must be an object"))?;
                let fields: &[&str] = match category {
                    "names" => &["resolver", "mode", "receiver"],
                    "predicates" => &["name", "receiver"],
                    _ => &["name", "input"],
                };
                let mut key = Vec::new();
                for field in fields {
                    key.push(
                        e.get(*field)
                            .ok_or_else(|| format!("hooks.{category} missing {field}"))?
                            .clone(),
                    );
                }
                let valid = match category {
                    "names" => {
                        e["resolver"].is_string()
                            && e["mode"]
                                .as_str()
                                .is_some_and(|m| ["name", "getter", "setter", "ref"].contains(&m))
                            && e.get("result")
                                .is_some_and(|r| r.is_string() || r.is_null())
                    }
                    "predicates" => {
                        e["name"].is_string() && e.get("result").is_some_and(Value::is_boolean)
                    }
                    _ => {
                        e["name"].is_string()
                            && e["input"].is_array()
                            && e.get("result").is_some_and(Value::is_array)
                    }
                };
                if !valid {
                    return Err(format!("invalid hooks.{category} entry"));
                }
                let encoded = serde_json::to_string(&key).map_err(|e| e.to_string())?;
                let result = &e["result"];
                if seen
                    .insert(encoded, result)
                    .is_some_and(|previous| previous != result)
                {
                    return Err(format!("conflicting hooks.{category} entries"));
                }
            }
        }
    }
    Ok(())
}

#[derive(Clone)]
struct Frame {
    value: Value,
    locals: Map<String, Value>,
}
struct Engine {
    root: PathBuf,
    graph: Graph,
    hooks: Value,
    native_cpp: Option<native_cpp::NativeCppResolver>,
    native_predicates: bool,
    native_sorters: bool,
    definitions: BTreeMap<String, Vec<Node>>,
    frames: Vec<Frame>,
    depth: usize,
    switches: Vec<(Value, bool, bool)>,
}
impl Engine {
    fn partial(&mut self, name: &str) -> Result<String, String> {
        if self.depth >= MAX_DEPTH {
            return Err("template recursion limit exceeded".into());
        }
        self.depth += 1;
        let result = (|| {
            let nodes = if let Some(n) = self.definitions.get(name) {
                n.clone()
            } else {
                let path = Path::new(name);
                if name.is_empty()
                    || path
                        .components()
                        .any(|c| !matches!(c, Component::Normal(_)))
                    || name.contains('\\')
                {
                    return Err(format!("invalid partial path {name}"));
                }
                let file = self.root.join(format!("{name}.mustache"));
                let canonical =
                    fs::canonicalize(&file).map_err(|e| format!("partial {name}: {e}"))?;
                if !canonical.starts_with(&self.root) {
                    return Err(format!("partial {name} escapes template root"));
                }
                let source =
                    fs::read_to_string(canonical).map_err(|e| format!("partial {name}: {e}"))?;
                parse(name, &source)?
            };
            self.collect_definitions(&nodes);
            self.nodes(&nodes)
        })();
        self.depth -= 1;
        result
    }
    fn collect_definitions(&mut self, nodes: &[Node]) {
        for node in nodes {
            match node {
                Node::Definition(name, body) => {
                    self.definitions.insert(name.clone(), body.clone());
                    self.collect_definitions(body);
                }
                Node::Section { body, .. } => self.collect_definitions(body),
                _ => {}
            }
        }
    }
    fn nodes(&mut self, nodes: &[Node]) -> Result<String, String> {
        let mut out = String::new();
        for node in nodes {
            let s = match node {
                Node::Text(s) => s.clone(),
                Node::Definition(..) => String::new(),
                Node::Partial(name, indent) => {
                    let value = self.partial(name)?;
                    if indent.is_empty() {
                        value
                    } else {
                        indent_lines(&value, indent)?
                    }
                }
                Node::Value(expr) => self.value(expr)?,
                Node::Section {
                    expression,
                    inverted,
                    body,
                } => self.section(expression, *inverted, body)?,
            };
            if out.len().saturating_add(s.len()) > MAX_OUTPUT {
                return Err("render output exceeds size limit".into());
            }
            out.push_str(&s);
        }
        Ok(out)
    }
    fn eval(&self, s: &str) -> Result<Value, String> {
        if s.starts_with('"') {
            if !s.ends_with('"') || s.len() < 2 {
                return Err(format!("invalid literal {s}"));
            }
            return Ok(Value::String(s[1..s.len() - 1].to_string()));
        }
        if s.starts_with('\'') && s.ends_with('\'') && s.len() >= 2 {
            return Ok(Value::String(s[1..s.len() - 1].to_string()));
        }
        match s {
            "true" => return Ok(Value::Bool(true)),
            "false" => return Ok(Value::Bool(false)),
            "null" => return Ok(Value::Null),
            _ => {}
        }
        if let Ok(n) = s.parse::<i64>() {
            return Ok(json!(n));
        }
        self.lookup(s)
    }
    fn lookup(&self, path: &str) -> Result<Value, String> {
        if path == "." || path == "this" {
            return Ok(self.current().clone());
        }
        let explicit = path.starts_with("this.") || path.starts_with("this[");
        let path = path
            .strip_prefix("this.")
            .or_else(|| path.strip_prefix("this").filter(|s| s.starts_with('[')))
            .unwrap_or(path);
        let parts = split_path(path)?;
        if parts.is_empty() {
            return Ok(self.current().clone());
        }
        let mut found = None;
        for frame in self.frames.iter().rev() {
            if let Some(v) = frame.locals.get(&parts[0]) {
                found = Some(v.clone());
                break;
            }
            match self.graph.property(&frame.value, &parts[0]) {
                Ok(Some(v)) => {
                    found = Some(v);
                    break;
                }
                Ok(None) => {}
                Err(e) => return Err(e),
            }
            if explicit {
                break;
            }
        }
        let mut value = match found {
            Some(v) => v,
            None => return Ok(Value::Null),
        };
        for p in &parts[1..] {
            if value.is_null() {
                return Ok(Value::Null);
            }
            value = self.graph.property(&value, p)?.unwrap_or(Value::Null);
        }
        Ok(value)
    }
    fn current(&self) -> &Value {
        &self.frames.last().expect("frame").value
    }
    fn push(
        &mut self,
        value: Value,
        locals: Map<String, Value>,
        body: &[Node],
    ) -> Result<String, String> {
        self.frames.push(Frame { value, locals });
        let result = self.nodes(body);
        self.frames.pop();
        result
    }
    fn args(&self, e: &Expression) -> Result<Vec<Value>, String> {
        e.args.iter().map(|s| self.eval(s)).collect()
    }
    fn hash(&self, e: &Expression, key: &str, default: &str) -> Result<String, String> {
        e.named
            .get(key)
            .map(|v| self.eval(v).and_then(|v| self.string_value(&v)))
            .unwrap_or_else(|| Ok(default.to_string()))
    }
    fn hook(
        &self,
        kind: &str,
        matches: impl Fn(&Value) -> bool,
        what: &str,
    ) -> Result<Value, String> {
        let entries = self
            .hooks
            .get(kind)
            .and_then(Value::as_array)
            .map(Vec::as_slice)
            .unwrap_or(&[]);
        let mut found = entries.iter().filter(|v| matches(v));
        let item = found
            .next()
            .ok_or_else(|| format!("missing replay {what}"))?;
        if found.any(|other| other.get("result") != item.get("result")) {
            return Err(format!("conflicting replay {what}"));
        }
        item.get("result")
            .cloned()
            .ok_or_else(|| format!("missing replay result for {what}"))
    }
    fn resolved_name(&self, args: &[Value]) -> Result<Value, String> {
        let (receiver, resolver, mode) = match args {
            [] => (self.current().clone(), String::new(), String::from("name")),
            [Value::String(s)] => (self.current().clone(), s.clone(), String::from("name")),
            [v] => (v.clone(), String::new(), String::from("name")),
            [v, key, rest @ ..] => (
                v.clone(),
                self.string_value(key)?,
                rest.first()
                    .map(|v| self.string_value(v))
                    .transpose()?
                    .unwrap_or_else(|| "name".to_string())
                    .to_lowercase(),
            ),
        };
        let mode = if ["getter", "setter", "ref"].contains(&mode.as_str()) {
            mode
        } else {
            "name".into()
        };
        if let Some(native) = &self.native_cpp {
            return native
                .resolve(&self.graph, &resolver, &mode, &receiver)
                .map(|result| result.map(Value::String).unwrap_or(Value::Null));
        }
        if receiver.is_null() {
            let registered = self
                .hooks
                .get("names")
                .and_then(Value::as_array)
                .is_some_and(|entries| {
                    entries.iter().any(|entry| {
                        entry.get("resolver").and_then(Value::as_str) == Some(&resolver)
                            && entry.get("mode").and_then(Value::as_str) == Some(&mode)
                    })
                });
            if !registered {
                return Err(format!(
                    "missing replay name resolver registration {resolver}/{mode}"
                ));
            }
            return Ok(Value::Null);
        }
        self.hook(
            "names",
            |v| {
                v.get("receiver") == Some(&receiver)
                    && v.get("resolver").and_then(Value::as_str) == Some(&resolver)
                    && v.get("mode").and_then(Value::as_str) == Some(&mode)
            },
            &format!("name resolver {resolver}/{mode} for {receiver}"),
        )
    }
    fn predicate(&self, name: &str, receiver: &Value) -> Result<bool, String> {
        if self.native_predicates {
            return native_controls::predicate(&self.graph, name, receiver);
        }
        self.hook(
            "predicates",
            |v| {
                v.get("receiver") == Some(receiver)
                    && v.get("name").and_then(Value::as_str) == Some(name)
            },
            &format!("predicate {name} for {receiver}"),
        )?
        .as_bool()
        .ok_or_else(|| format!("predicate {name} result must be boolean"))
    }
    fn require_predicate(&self, name: &str) -> Result<(), String> {
        if self.native_predicates {
            return native_controls::require_predicate(name);
        }
        let registered = self
            .hooks
            .get("registered_predicates")
            .and_then(Value::as_array)
            .is_some_and(|values| values.iter().any(|v| v.as_str() == Some(name)))
            || self
                .hooks
                .get("predicates")
                .and_then(Value::as_array)
                .is_some_and(|values| {
                    values
                        .iter()
                        .any(|v| v.get("name").and_then(Value::as_str) == Some(name))
                });
        if !registered {
            return Err(format!("missing replay predicate registration {name}"));
        }
        Ok(())
    }
    fn eval_path(&self, args: &[Value]) -> Result<Value, String> {
        if args.is_empty() || args.iter().any(Value::is_null) {
            return Ok(Value::Null);
        }
        let path = self.string_value(&args[0])?;
        let mut value = self.lookup(&path)?;
        for arg in &args[1..] {
            if value.is_null() {
                return Ok(Value::Null);
            }
            value = self
                .graph
                .property(&value, &self.string_value(arg)?)?
                .unwrap_or(Value::Null);
        }
        Ok(value)
    }
    fn string_value(&self, value: &Value) -> Result<String, String> {
        match value {
            Value::Object(m) if m.contains_key("enum") => self
                .graph
                .property(value, "toString")?
                .and_then(|v| v.as_str().map(str::to_owned))
                .ok_or_else(|| "unsupported enum string conversion".into()),
            Value::Object(_) | Value::Array(_) => {
                Err("unsupported object string conversion".into())
            }
            _ => Ok(display(value)),
        }
    }
    fn value(&mut self, input: &str) -> Result<String, String> {
        let e = expression(input)?;
        let args = self.args(&e)?;
        let allowed: &[&str] = match e.name.as_str() {
            "prefix" | "prefixPartial" => &["skipFirstLine"],
            "join" => &["delimiter", "lambda"],
            _ => &[],
        };
        check_hash(&e, allowed)?;
        match e.name.as_str() {
            "resolveName" => Ok(display(&self.resolved_name(&args)?)),
            "eval" => self.string_value(&self.eval_path(&args)?),
            "prefix" | "prefixPartial" => {
                if args.is_empty() {
                    return Ok(String::new());
                }
                let value = if e.name == "prefixPartial" {
                    self.partial(&self.string_value(&args[0])?)?
                } else {
                    self.string_value(&args[0])?
                };
                let prefix = args
                    .get(1)
                    .map(|v| self.string_value(v))
                    .transpose()?
                    .unwrap_or_default();
                let skip = self
                    .hash(&e, "skipFirstLine", "false")?
                    .eq_ignore_ascii_case("true");
                let value = value.replace("\r\n", "\n").replace('\r', "\n");
                let mut out = String::new();
                for (i, line) in value.split('\n').enumerate() {
                    if i > 0 {
                        append_checked(&mut out, "\n")?;
                    }
                    let p = if i == 0 && skip { "" } else { &prefix };
                    let trimmed = line.trim_end();
                    if trimmed.is_empty() {
                        append_checked(&mut out, p.trim_end())?;
                    } else {
                        append_checked(&mut out, p)?;
                        append_checked(&mut out, trimmed)?;
                    }
                }
                Ok(out)
            }
            "joinPartial" => {
                if args.len() < 2 {
                    return Ok(String::new());
                }
                if args[0].is_null() || args[1].is_null() {
                    return Err("joinPartial requires non-null collection and partial name".into());
                }
                let values = args[0]
                    .as_array()
                    .cloned()
                    .unwrap_or_else(|| vec![args[0].clone()]);
                let delimiter = args
                    .get(2)
                    .map(|v| self.string_value(v))
                    .transpose()?
                    .unwrap_or_default();
                let mut out = String::new();
                for (i, v) in values.into_iter().enumerate() {
                    self.frames.push(Frame {
                        value: v,
                        locals: Map::new(),
                    });
                    let item = self.partial(&self.string_value(&args[1])?);
                    self.frames.pop();
                    let item = item?;
                    if i > 0 {
                        append_checked(&mut out, &delimiter)?;
                    }
                    append_checked(&mut out, &item)?;
                }
                Ok(out)
            }
            "join" => {
                if e.named.contains_key("lambda") {
                    return Err("unsupported join lambda".into());
                }
                let delimiter = self.hash(&e, "delimiter", "")?;
                let mut out = String::new();
                for (i, value) in args.iter().enumerate() {
                    if i > 0 {
                        append_checked(&mut out, &delimiter)?;
                    }
                    if let Value::Array(items) = value {
                        for (j, item) in items.iter().enumerate() {
                            if j > 0 {
                                append_checked(&mut out, &delimiter)?;
                            }
                            append_checked(&mut out, &self.string_value(item)?)?;
                        }
                    } else {
                        append_checked(&mut out, &self.string_value(value)?)?;
                    }
                }
                Ok(out)
            }
            "include" => {
                let name = args.first().ok_or("include expects partial name")?;
                self.partial(&self.string_value(name)?)
            }
            "capitalize" => {
                if args.first().is_some_and(Value::is_null) {
                    return Err("capitalize requires a non-null value".into());
                }
                let s = args
                    .first()
                    .map(|v| self.string_value(v))
                    .transpose()?
                    .unwrap_or_default();
                let mut chars = s.chars();
                match chars.next() {
                    None => Ok(String::new()),
                    Some(c) if c.is_ascii() => {
                        Ok(format!("{}{}", c.to_ascii_uppercase(), chars.as_str()))
                    }
                    Some('ß') => Ok(format!("Ss{}", chars.as_str())),
                    Some(c) => Err(format!(
                        "unsupported Unicode titlecase for U+{:04X}",
                        c as u32
                    )),
                }
            }
            "escape" => {
                if args.first().is_some_and(Value::is_null) {
                    return Err("escape requires a non-null value".into());
                }
                let s = args
                    .first()
                    .map(|v| self.string_value(v))
                    .transpose()?
                    .unwrap_or_default();
                let mut out = String::new();
                for c in s.chars() {
                    match c {
                        '\\' => append_checked(&mut out, "\\\\")?,
                        '"' => append_checked(&mut out, "\\\"")?,
                        '\n' => append_checked(&mut out, "\\n")?,
                        '\r' => append_checked(&mut out, "\\r")?,
                        '\t' => append_checked(&mut out, "\\t")?,
                        '\u{8}' => append_checked(&mut out, "\\b")?,
                        _ => append_checked(&mut out, c.encode_utf8(&mut [0; 4]))?,
                    }
                }
                Ok(out)
            }
            _ if e.args.is_empty() && e.named.is_empty() => {
                self.string_value(&self.lookup(&e.name)?)
            }
            _ => Err(format!("unsupported helper {}", e.name)),
        }
    }
    fn section(&mut self, input: &str, inverted: bool, body: &[Node]) -> Result<String, String> {
        let e = expression(input)?;
        let args = self.args(&e)?;
        let allowed: &[&str] = match e.name.as_str() {
            "if" | "unless" => &["logic"],
            "prefix" | "prefixPartial" => &["skipFirstLine"],
            "set" => &[],
            "setJoin" => &["delimiter"],
            "sort" => &["sorter"],
            "filter" => &["predicate"],
            "case" => &["break"],
            _ => &[],
        };
        if e.name != "set" {
            check_hash(&e, allowed)?;
        }
        if inverted {
            let value = self.lookup(&e.name)?;
            return if !truth(&value) {
                self.nodes(body)
            } else {
                Ok(String::new())
            };
        }
        match e.name.as_str() {
            "prefix" | "prefixPartial" | "joinPartial" | "capitalize" | "escape" => {
                self.value(input)
            }
            "if" | "unless" => {
                let logic = self.hash(&e, "logic", if e.name == "if" { "and" } else { "or" })?;
                let matching = |v: &Value| helper_truth(v) == (e.name == "if");
                let result = match logic.as_str() {
                    "and" => args.iter().all(matching),
                    "or" => args.iter().any(matching),
                    _ => return Err(format!("unsupported if logic {logic}")),
                };
                if result {
                    self.nodes(body)
                } else {
                    Ok(String::new())
                }
            }
            "set" => {
                let mut locals = Map::new();
                for (k, v) in &e.named {
                    locals.insert(k.clone(), self.eval(v)?);
                }
                self.push(Value::Object(locals), Map::new(), body)
            }
            "setJoin" => {
                let key = args.first().ok_or("setJoin requires a key")?;
                let delimiter = self.hash(&e, "delimiter", "")?;
                let mut value = String::new();
                for (i, item) in args.iter().skip(1).filter(|v| !v.is_null()).enumerate() {
                    if i > 0 {
                        append_checked(&mut value, &delimiter)?;
                    }
                    append_checked(&mut value, &self.string_value(item)?)?;
                }
                let mut locals = Map::new();
                locals.insert(self.string_value(key)?, Value::String(value));
                self.push(Value::Object(locals), Map::new(), body)
            }
            "resolveName" => {
                let v = self.resolved_name(&args)?;
                if v.is_null() {
                    Ok(String::new())
                } else {
                    self.push(v, Map::new(), body)
                }
            }
            "ifPredicate" | "unlessPredicate" => {
                let (receiver, name) = match args.as_slice() {
                    [Value::String(name), ..] => (self.current().clone(), name.clone()),
                    [v, name, ..] => (v.clone(), self.string_value(name)?),
                    _ => return Err(format!("{} requires a predicate name", e.name)),
                };
                self.require_predicate(&name)?;
                if receiver.is_null() {
                    return Ok(String::new());
                }
                if self.predicate(&name, &receiver)? == (e.name == "ifPredicate") {
                    self.nodes(body)
                } else {
                    Ok(String::new())
                }
            }
            "instanceOf" | "notInstanceOf" => {
                if args.len() < 2 {
                    return Err(format!("{} requires two arguments", e.name));
                }
                let class = self
                    .graph
                    .class(&args[0])
                    .ok_or("instanceOf requires a model or enum value")?;
                if class.ends_with(&self.string_value(&args[1])?) == (e.name == "instanceOf") {
                    self.nodes(body)
                } else {
                    Ok(String::new())
                }
            }
            "isEq" | "isNotEq" => {
                if args.len() < 2 {
                    return Err(format!("{} requires two arguments", e.name));
                }
                if args[0].is_null() || args[1].is_null() {
                    return Ok(String::new());
                }
                if (args[0] == args[1]) == (e.name == "isEq") {
                    self.nodes(body)
                } else {
                    Ok(String::new())
                }
            }
            "each" => {
                let args = if args.is_empty() {
                    vec![self.current().clone()]
                } else {
                    args
                };
                if args.iter().any(|v| !v.is_array() && !v.is_null()) {
                    return Err("each requires iterable arguments".into());
                }
                let values: Vec<_> = args
                    .iter()
                    .filter_map(Value::as_array)
                    .flatten()
                    .cloned()
                    .collect();
                self.iterate(&values, body)
            }
            "sort" => {
                let values: Vec<_> = args
                    .iter()
                    .filter_map(Value::as_array)
                    .flatten()
                    .filter(|v| !v.is_null())
                    .cloned()
                    .collect();
                let sorter = self.hash(&e, "sorter", "")?;
                let sorted = if self.native_sorters {
                    Value::Array(native_controls::sort(&self.graph, &sorter, &values)?)
                } else {
                    self.hook(
                        "sorters",
                        |v| {
                            v.get("name").and_then(Value::as_str) == Some(&sorter)
                                && v.get("input") == Some(&Value::Array(values.clone()))
                        },
                        &format!("sorter {sorter}"),
                    )?
                };
                let sorted = sorted.as_array().ok_or("sorter result must be a list")?;
                let mut output = String::new();
                for value in sorted {
                    let item = self.push(value.clone(), Map::new(), body)?;
                    if output.len().saturating_add(item.len()) > MAX_OUTPUT {
                        return Err("render output exceeds size limit".into());
                    }
                    output.push_str(&item);
                }
                Ok(output)
            }
            "filter" => {
                let predicate = self.hash(&e, "predicate", "")?;
                if predicate.is_empty() {
                    return Err("filter requires predicate".into());
                }
                self.require_predicate(&predicate)?;
                let mut values = Vec::new();
                for v in args
                    .iter()
                    .filter_map(Value::as_array)
                    .flatten()
                    .filter(|v| !v.is_null())
                {
                    if self.predicate(&predicate, v)? {
                        values.push(v.clone());
                    }
                }
                self.push(Value::Array(values), Map::new(), body)
            }
            "eval" => {
                let value = self.eval_path(&args)?;
                if !value.is_null() {
                    self.push(value, Map::new(), body)
                } else {
                    Ok(String::new())
                }
            }
            "switch" => {
                let value = args
                    .first()
                    .cloned()
                    .unwrap_or_else(|| self.current().clone());
                if value.is_null() {
                    return Ok(String::new());
                }
                self.switches.push((value, false, false));
                let result = self.nodes(body);
                self.switches.pop();
                result
            }
            "case" => {
                let (value, terminated, fallthrough) =
                    self.switches.last().cloned().ok_or("case outside switch")?;
                let target = args.first().ok_or("case requires a value")?;
                if !terminated && (fallthrough || &value == target) {
                    let result = self.nodes(body)?;
                    let should_break = self.hash(&e, "break", "true")? == "true";
                    let state = self.switches.last_mut().ok_or("case outside switch")?;
                    state.1 = should_break;
                    state.2 = true;
                    Ok(result)
                } else {
                    Ok(String::new())
                }
            }
            "default" => {
                let (_, terminated, _) = self.switches.last().ok_or("default outside switch")?;
                if !terminated {
                    let result = self.nodes(body)?;
                    if let Some(state) = self.switches.last_mut() {
                        state.1 = true;
                    }
                    Ok(result)
                } else {
                    Ok(String::new())
                }
            }
            "numExpr" => Err("unsupported helper numExpr".into()),
            _ if !e.args.is_empty() || !e.named.is_empty() => {
                Err(format!("unsupported helper {}", e.name))
            }
            _ => {
                let value = self.lookup(&e.name)?;
                match &value {
                    Value::Array(a) => self.iterate(a, body),
                    _ if truth(&value) => self.push(value, Map::new(), body),
                    _ => Ok(String::new()),
                }
            }
        }
    }
    fn iterate(&mut self, values: &[Value], body: &[Node]) -> Result<String, String> {
        let mut out = String::new();
        for (i, v) in values.iter().enumerate() {
            let mut locals = Map::new();
            locals.insert("iter".into(), json!({"index": i+1, "position": i, "hasNext": i+1 < values.len(), "hasPrevious": i > 0, "first": i == 0, "last": i+1 == values.len(), "isFirst": i == 0, "isLast": i+1 == values.len()}));
            let item = self.push(v.clone(), locals, body)?;
            if out.len().saturating_add(item.len()) > MAX_OUTPUT {
                return Err("render output exceeds size limit".into());
            }
            out.push_str(&item);
        }
        Ok(out)
    }
}
fn split_path(path: &str) -> Result<Vec<String>, String> {
    let mut parts = Vec::new();
    let mut current = String::new();
    let mut bracket = false;
    for c in path.chars() {
        match c {
            '[' if !bracket => {
                if !current.is_empty() {
                    parts.push(std::mem::take(&mut current));
                }
                bracket = true;
            }
            ']' if bracket => {
                if !current.is_empty() {
                    parts.push(
                        std::mem::take(&mut current)
                            .trim_matches(['\'', '"'])
                            .to_string(),
                    );
                }
                bracket = false;
            }
            '.' if !bracket => {
                if !current.is_empty() {
                    parts.push(std::mem::take(&mut current));
                }
            }
            '[' | ']' => return Err(format!("invalid selector {path}")),
            _ => current.push(c),
        }
    }
    if bracket {
        return Err(format!("invalid selector {path}"));
    }
    if !current.is_empty() {
        parts.push(current);
    }
    Ok(parts)
}
fn check_hash(e: &Expression, allowed: &[&str]) -> Result<(), String> {
    if let Some(key) = e.named.keys().find(|key| !allowed.contains(&key.as_str())) {
        return Err(format!("unsupported option {key} for {}", e.name));
    }
    Ok(())
}
fn truth(v: &Value) -> bool {
    match v {
        Value::Null => false,
        Value::Bool(b) => *b,
        Value::Array(a) => !a.is_empty(),
        _ => true,
    }
}
fn helper_truth(v: &Value) -> bool {
    match v {
        Value::String(s) => !s.is_empty(),
        Value::Number(n) => n.as_f64().is_some_and(|x| x != 0.0),
        _ => truth(v),
    }
}
fn display(v: &Value) -> String {
    match v {
        Value::Null => String::new(),
        Value::String(s) => s.clone(),
        Value::Bool(b) => b.to_string(),
        Value::Number(n) => n.to_string(),
        Value::Object(m) if m.contains_key("enum") => m
            .get("name")
            .and_then(Value::as_str)
            .unwrap_or("")
            .to_string(),
        _ => v.to_string(),
    }
}
fn append_checked(output: &mut String, value: &str) -> Result<(), String> {
    if output.len().saturating_add(value.len()) > MAX_OUTPUT {
        return Err("render output exceeds size limit".into());
    }
    output.push_str(value);
    Ok(())
}
fn indent_lines(value: &str, indent: &str) -> Result<String, String> {
    let mut out = String::new();
    for line in value.split_inclusive('\n') {
        append_checked(&mut out, indent)?;
        append_checked(&mut out, line)?;
    }
    Ok(out)
}
