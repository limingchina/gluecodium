//! A bounded Trimou-compatible renderer for explicit reference snapshots.
mod graph;
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
        if !["names", "predicates", "sorters"].contains(&category.as_str()) {
            return Err(format!("unsupported hook category {category}"));
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
                        indent_lines(&value, indent)
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
            return serde_json::from_str(s).map_err(|e| format!("invalid literal {s}: {e}"));
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
            .map(|v| self.eval(v).map(|v| display(&v)))
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
                key.as_str().unwrap_or("").to_string(),
                rest.first()
                    .and_then(Value::as_str)
                    .unwrap_or("name")
                    .to_lowercase(),
            ),
        };
        if receiver.is_null() {
            return Ok(Value::Null);
        }
        let mode = if ["getter", "setter", "ref"].contains(&mode.as_str()) {
            mode
        } else {
            "name".into()
        };
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
    fn eval_path(&self, args: &[Value]) -> Result<Value, String> {
        if args.is_empty() || args.iter().any(Value::is_null) {
            return Ok(Value::Null);
        }
        let mut path = display(&args[0]);
        for arg in &args[1..] {
            path.push('[');
            path.push_str(&display(arg));
            path.push(']');
        }
        self.lookup(&path)
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
            "eval" => Ok(display(&self.eval_path(&args)?)),
            "prefix" | "prefixPartial" => {
                if args.is_empty() {
                    return Ok(String::new());
                }
                let value = if e.name == "prefixPartial" {
                    self.partial(&display(&args[0]))?
                } else {
                    display(&args[0])
                };
                let prefix = args.get(1).map(display).unwrap_or_default();
                let skip = self.hash(&e, "skipFirstLine", "false")? == "true";
                let value = value.replace("\r\n", "\n").replace('\r', "\n");
                Ok(value
                    .split('\n')
                    .enumerate()
                    .map(|(i, l)| {
                        format!("{}{}", if i == 0 && skip { "" } else { &prefix }, l)
                            .trim_end()
                            .to_string()
                    })
                    .collect::<Vec<_>>()
                    .join("\n"))
            }
            "joinPartial" => {
                if args.len() < 2 {
                    return Ok(String::new());
                }
                let values = args[0]
                    .as_array()
                    .cloned()
                    .unwrap_or_else(|| vec![args[0].clone()]);
                let mut out = Vec::new();
                for v in values {
                    self.frames.push(Frame {
                        value: v,
                        locals: Map::new(),
                    });
                    let item = self.partial(&display(&args[1]));
                    self.frames.pop();
                    out.push(item?);
                }
                Ok(out.join(&args.get(2).map(display).unwrap_or_default()))
            }
            "join" => {
                if e.named.contains_key("lambda") {
                    return Err("unsupported join lambda".into());
                }
                let delimiter = self.hash(&e, "delimiter", "")?;
                let values = args
                    .iter()
                    .map(|v| match v {
                        Value::Array(a) => {
                            a.iter().map(display).collect::<Vec<_>>().join(&delimiter)
                        }
                        Value::Null => String::new(),
                        _ => display(v),
                    })
                    .collect::<Vec<_>>();
                Ok(values.join(&delimiter))
            }
            "include" => {
                let name = args.first().ok_or("include expects partial name")?;
                self.partial(&display(name))
            }
            "capitalize" => {
                let s = args.first().map(display).unwrap_or_default();
                let mut chars = s.chars();
                Ok(chars
                    .next()
                    .map(|c| c.to_uppercase().collect::<String>() + chars.as_str())
                    .unwrap_or_default())
            }
            "escape" => {
                let s = args.first().map(display).unwrap_or_default();
                Ok(s.replace('\\', "\\\\")
                    .replace('"', "\\\"")
                    .replace('\n', "\\n")
                    .replace('\r', "\\r")
                    .replace('\t', "\\t"))
            }
            _ if e.args.is_empty() && e.named.is_empty() => Ok(display(&self.eval(&e.name)?)),
            _ => Err(format!("unsupported helper {}", e.name)),
        }
    }
    fn section(&mut self, input: &str, inverted: bool, body: &[Node]) -> Result<String, String> {
        let e = expression(input)?;
        let args = self.args(&e)?;
        let allowed: &[&str] = match e.name.as_str() {
            "if" | "unless" => &["logic"],
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
            let value = self.eval(&e.name)?;
            return if !truth(&value) {
                self.nodes(body)
            } else {
                Ok(String::new())
            };
        }
        match e.name.as_str() {
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
                let value = args
                    .iter()
                    .skip(1)
                    .filter(|v| !v.is_null())
                    .map(display)
                    .collect::<Vec<_>>()
                    .join(&delimiter);
                let mut locals = Map::new();
                locals.insert(display(key), Value::String(value));
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
                    [v, name, ..] => (v.clone(), display(name)),
                    _ => return Err(format!("{} requires a predicate name", e.name)),
                };
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
                if class.ends_with(&display(&args[1])) == (e.name == "instanceOf") {
                    self.nodes(body)
                } else {
                    Ok(String::new())
                }
            }
            "isEq" | "isNotEq" => {
                if args.len() < 2 {
                    return Err(format!("{} requires two arguments", e.name));
                }
                if (args[0] == args[1]) == (e.name == "isEq") {
                    self.nodes(body)
                } else {
                    Ok(String::new())
                }
            }
            "each" => {
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
                let sorted = self.hook(
                    "sorters",
                    |v| {
                        v.get("name").and_then(Value::as_str) == Some(&sorter)
                            && v.get("input") == Some(&Value::Array(values.clone()))
                    },
                    &format!("sorter {sorter}"),
                )?;
                let sorted = sorted.as_array().ok_or("sorter result must be a list")?;
                self.iterate(sorted, body)
            }
            "filter" => {
                let predicate = self.hash(&e, "predicate", "")?;
                if predicate.is_empty() {
                    return Err("filter requires predicate".into());
                }
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
                    self.nodes(body)
                } else {
                    Ok(String::new())
                }
            }
            "numExpr" => Err("unsupported helper numExpr".into()),
            _ if !e.args.is_empty() || !e.named.is_empty() => {
                Err(format!("unsupported helper {}", e.name))
            }
            _ => {
                let value = self.eval(&e.name)?;
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
            locals.insert("iter".into(), json!({"index": i+1, "position": i+1, "hasNext": i+1 < values.len(), "hasPrevious": i > 0, "first": i == 0, "last": i+1 == values.len(), "isFirst": i == 0, "isLast": i+1 == values.len()}));
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
fn indent_lines(value: &str, indent: &str) -> String {
    value
        .split_inclusive('\n')
        .map(|s| format!("{indent}{s}"))
        .collect()
}
