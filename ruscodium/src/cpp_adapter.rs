//! Native LIME to the existing C++ compatibility generator.
mod docs;
use crate::{cpp_generation, Decl, Model, TypeRef};
use serde::{Deserialize, Serialize};
use serde_json::{json, Map, Value};
use std::{
    collections::{BTreeMap, BTreeSet},
    path::Path,
};

#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Options {
    #[serde(default)]
    pub root_namespace: Vec<String>,
    #[serde(default)]
    pub internal_namespace: Vec<String>,
    #[serde(default = "default_export")]
    pub export: String,
    #[serde(default)]
    pub export_common: Option<String>,
    #[serde(default)]
    pub copyright_header: Option<String>,
    #[serde(default)]
    pub tags: Vec<String>,
    #[serde(default)]
    pub name_rules: BTreeMap<String, String>,
    #[serde(default)]
    pub werror: Vec<String>,
    #[serde(default, skip_serializing)]
    pub strict: bool,
    #[serde(default, skip_serializing)]
    pub docs_placeholders: BTreeMap<String, String>,
}
fn default_export() -> String {
    "_GLUECODIUM_CPP".into()
}
impl Default for Options {
    fn default() -> Self {
        Self {
            root_namespace: vec![],
            internal_namespace: vec![],
            export: default_export(),
            export_common: None,
            copyright_header: None,
            tags: vec![],
            name_rules: BTreeMap::new(),
            werror: vec![],
            strict: false,
            docs_placeholders: BTreeMap::new(),
        }
    }
}

const BASIC: &[(&str, &str)] = &[
    ("Blob", "BLOB"),
    ("Boolean", "BOOLEAN"),
    ("Byte", "INT8"),
    ("Date", "DATE"),
    ("Double", "DOUBLE"),
    ("Duration", "DURATION"),
    ("Float", "FLOAT"),
    ("Int", "INT32"),
    ("Locale", "LOCALE"),
    ("Long", "INT64"),
    ("Short", "INT16"),
    ("String", "STRING"),
    ("UByte", "UINT8"),
    ("UInt", "UINT32"),
    ("ULong", "UINT64"),
    ("UShort", "UINT16"),
    ("Void", "VOID"),
];
// The parser strips LIME backticks, so model paths can contain spaces,
// punctuation and Unicode even when their generated C++ names are overridden.
fn valid_ident(s: &str) -> bool {
    !s.is_empty() && !s.chars().any(char::is_control)
}
fn valid_qualified(s: &str) -> bool {
    !s.is_empty() && s.split('.').all(valid_ident)
}
// Convert source annotations as the LIME loader does. Repeated values accumulate.
fn annotation_map(annotations: &[crate::Annotation]) -> Result<Map<String, Value>, String> {
    fn key(s: &str) -> String {
        let mut out = String::new();
        for (i, c) in s.chars().enumerate() {
            if i > 0 && c.is_ascii_uppercase() {
                out.push('_');
            }
            out.push(c.to_ascii_uppercase());
        }
        out
    }
    fn add(map: &mut Map<String, Value>, attribute: &str, value_key: &str, value: Value) {
        let values = map
            .entry(attribute.to_owned())
            .or_insert_with(|| json!({}))
            .as_object_mut()
            .unwrap();
        match values.get_mut(value_key) {
            None => {
                values.insert(value_key.into(), value);
            }
            Some(old) if *old == Value::Bool(true) => *old = value,
            Some(old) => {
                let mut list = match old.take() {
                    Value::Array(a) => a,
                    other => vec![other],
                };
                match value {
                    Value::Array(a) => list.extend(a),
                    other => list.push(other),
                }
                *old = Value::Array(list);
            }
        }
    }
    let mut attrs = Map::new();
    for annotation in annotations {
        let attr = key(&annotation.name);
        if ![
            "AFTER_CONSTRUCTION",
            "CPP",
            "JAVA",
            "KOTLIN",
            "SWIFT",
            "DART",
            "ASYNC",
            "ASYNC_DECORATOR",
            "ASYNC_TASK_HANDLE",
            "CACHED",
            "DEPRECATED",
            "ENABLE_IF",
            "EQUATABLE",
            "IMMUTABLE",
            "INTERNAL",
            "NO_CACHE",
            "OPTIMIZED",
            "OVERLOADED",
            "SERIALIZABLE",
            "SKIP",
        ]
        .contains(&attr.as_str())
        {
            return Err(format!("unsupported annotation {}", annotation.name));
        }
        if annotation.values.is_empty() {
            attrs.entry(attr).or_insert_with(|| json!({}));
            continue;
        }
        for entry in &annotation.values {
            let mut decoded = Vec::new();
            for v in &entry.values {
                let v = crate::decode_lime_string(v).map_err(|_| "invalid annotation string")?;
                decoded.push(Value::String(
                    if attr == "DEPRECATED" || attr == "AFTER_CONSTRUCTION" {
                        v
                    } else {
                        v.trim().replace(['\r', '\n'], "")
                    },
                ));
            }
            let value = match decoded.len() {
                0 => Value::Bool(true),
                1 => decoded.remove(0),
                _ => Value::Array(decoded),
            };
            if attr == "SKIP" || attr == "ENABLE_IF" || attr == "INTERNAL" {
                let source = if entry
                    .name
                    .as_deref()
                    .is_some_and(|s| !s.eq_ignore_ascii_case("tag"))
                {
                    Value::String(entry.name.clone().unwrap())
                } else {
                    value
                };
                let items = match source {
                    Value::Array(a) => a,
                    v => vec![v],
                };
                for item in items {
                    if attr == "INTERNAL" && item == Value::Bool(true) {
                        attrs.entry(attr.clone()).or_insert_with(|| json!({}));
                        continue;
                    }
                    let Some(tag) = item.as_str() else { continue };
                    let platform = tag.to_ascii_uppercase();
                    if attr == "SKIP"
                        && ["CPP", "JAVA", "KOTLIN", "SWIFT", "DART"].contains(&platform.as_str())
                    {
                        add(&mut attrs, &platform, "SKIP", json!(true));
                    } else if attr == "INTERNAL"
                        && ["CPP", "JAVA", "KOTLIN", "SWIFT", "DART"].contains(&platform.as_str())
                    {
                        add(&mut attrs, &platform, "INTERNAL", json!(true));
                    } else if attr != "INTERNAL" {
                        add(&mut attrs, &attr, "TAG", json!(tag));
                    }
                }
                continue;
            }
            let value_key =
                entry
                    .name
                    .as_ref()
                    .map(|v| key(v))
                    .unwrap_or_else(|| match attr.as_str() {
                        "CPP" | "JAVA" | "KOTLIN" | "SWIFT" | "DART" | "ASYNC_TASK_HANDLE" => {
                            "NAME".into()
                        }
                        "DEPRECATED" => "MESSAGE".into(),
                        "AFTER_CONSTRUCTION" => "FUNCTION".into(),
                        _ => "".into(),
                    });
            if value_key.is_empty() {
                return Err(format!(
                    "annotation {} does not support default values",
                    annotation.name
                ));
            }
            add(&mut attrs, &attr, &value_key, value);
        }
    }
    Ok(attrs)
}
fn filter_declarations(decls: &mut Vec<Decl>, tags: &[String], cpp: bool) -> Result<(), String> {
    fn matches(value: Option<&Value>, tags: &[String]) -> Option<bool> {
        match value {
            Some(Value::Bool(true)) => Some(true),
            Some(Value::String(s)) => Some(tags.iter().any(|t| t.eq_ignore_ascii_case(s))),
            Some(Value::Array(a)) => Some(
                a.iter()
                    .filter_map(Value::as_str)
                    .any(|s| tags.iter().any(|t| t.eq_ignore_ascii_case(s))),
            ),
            _ => None,
        }
    }
    let mut kept = Vec::new();
    for mut d in decls.drain(..) {
        let attrs = annotation_map(&d.annotations)?;
        let get = |a: &str, k: &str| attrs.get(a).and_then(|v| v.get(k));
        let keep = if cpp {
            matches(get("CPP", "ENABLE_IF"), tags) != Some(false)
                && matches(get("CPP", "SKIP"), tags) != Some(true)
        } else {
            matches(get("ENABLE_IF", "TAG"), tags) != Some(false)
                && matches(get("SKIP", "TAG"), tags) != Some(true)
        };
        if keep {
            if d.kind != "property" {
                filter_declarations(&mut d.children, tags, cpp)?;
            }
            kept.push(d);
        }
    }
    *decls = kept;
    Ok(())
}
fn validate_cpp_skip(decls: &[Decl]) -> Result<(), String> {
    for d in decls {
        let attrs = annotation_map(&d.annotations)?;
        let skip = attrs.get("CPP").and_then(|v| v.get("SKIP"));
        if skip.is_some_and(|v| *v != Value::Bool(false))
            && !matches!(d.kind.as_str(), "field_constructor" | "const")
        {
            return Err(format!(
                "C++ skip validation failed: @Cpp(Skip) is invalid on {}",
                d.name
            ));
        }
        validate_cpp_skip(&d.children)?;
        validate_cpp_skip(&d.params)?;
    }
    Ok(())
}
fn validate_strict(decls: &[Decl]) -> Result<(), String> {
    for d in decls {
        if d.kind == "struct"
            && !d
                .children
                .iter()
                .any(|c| matches!(c.kind.as_str(), "constructor" | "field_constructor"))
        {
            let attrs = annotation_map(&d.annotations)?;
            if attrs.contains_key("IMMUTABLE") {
                return Err(format!("strict validation failed: immutable struct {} requires an explicit constructor", d.name));
            }
            if !attrs.contains_key("INTERNAL") {
                for field in d.children.iter().filter(|c| c.kind == "field") {
                    if annotation_map(&field.annotations)?.contains_key("INTERNAL")
                        && field.literal.is_none()
                        && !field.ty.as_ref().is_some_and(|t| t.nullable)
                    {
                        return Err(format!("strict validation failed: struct {} has an internal field without a default or explicit constructor", d.name));
                    }
                }
            }
        }
        validate_strict(&d.children)?;
    }
    Ok(())
}
fn guard_type(t: &mut TypeRef) -> Result<(), String> {
    if !t.docs.is_empty() {
        return Err("documentation is not valid inside a type reference".into());
    }
    let builtin = BASIC.iter().any(|(n, _)| *n == t.name)
        || ["List", "Set", "Map"].contains(&t.name.as_str());
    if t.builtin != builtin || !valid_qualified(&t.name) {
        return Err(format!("invalid type reference {}", t.name));
    }
    let arity = match t.name.as_str() {
        "List" | "Set" => 1,
        "Map" => 2,
        _ => 0,
    };
    if t.args.len() != arity {
        return Err(format!("invalid type arguments for {}", t.name));
    }
    t.resolved = None;
    for arg in &mut t.args {
        guard_type(arg)?;
    }
    Ok(())
}
fn guard_decl(d: &mut Decl, parent: &str) -> Result<(), String> {
    let allowed = match parent {
        "file" => matches!(
            d.kind.as_str(),
            "class" | "interface" | "struct" | "enum" | "typealias" | "lambda" | "exception"
        ),
        "class" | "interface" => matches!(
            d.kind.as_str(),
            "class"
                | "interface"
                | "struct"
                | "enum"
                | "typealias"
                | "lambda"
                | "exception"
                | "const"
                | "fun"
                | "constructor"
                | "property"
        ),
        "struct" => matches!(
            d.kind.as_str(),
            "class"
                | "interface"
                | "struct"
                | "enum"
                | "typealias"
                | "lambda"
                | "exception"
                | "const"
                | "fun"
                | "constructor"
                | "field"
                | "field_constructor"
        ),
        "enum" => d.kind == "enumerator",
        "fun" | "constructor" | "field_constructor" | "lambda" => d.kind == "parameter",
        "property" => d.kind == "accessor",
        _ => false,
    };
    if !allowed {
        return Err(format!("unsupported {} in {parent}", d.kind));
    }
    if !(valid_ident(&d.name) || (parent == "lambda" && d.name.is_empty())) {
        return Err(format!("invalid {} name {:?}", d.kind, d.name));
    }
    docs::parse_documentation(&d.docs)?;
    for annotation in &d.annotations {
        let source = format!("package verify\n{}\nclass Example {{}}\n", annotation.raw);
        let parsed = crate::parse("<annotation>", &source, false)
            .map_err(|_| "invalid annotation source")?;
        let actual = parsed
            .declarations
            .first()
            .and_then(|d| d.annotations.first())
            .ok_or("invalid annotation source")?;
        if parsed.declarations.len() != 1
            || actual.name != annotation.name
            || actual.raw != annotation.raw
            || actual.values.len() != annotation.values.len()
            || actual
                .values
                .iter()
                .zip(&annotation.values)
                .any(|(a, b)| a.name != b.name || a.values != b.values)
        {
            return Err("inconsistent annotation source".into());
        }
    }
    if !d.parents.is_empty() && !matches!(d.kind.as_str(), "class" | "interface") {
        return Err("invalid inheritance placement".into());
    }
    if parent == "lambda" && !d.annotations.is_empty() {
        return Err("lambda parameter annotations belong on its type".into());
    }
    if d.kind == "exception" && d.ty.as_ref().is_some_and(|t| t.nullable) {
        return Err("exception payload cannot be nullable".into());
    }
    for parent in &mut d.parents {
        guard_type(parent)?;
    }
    if let Some(t) = &mut d.throws {
        if !matches!(d.kind.as_str(), "fun" | "constructor")
            || !matches!(parent, "class" | "interface" | "struct")
            || t.nullable
        {
            return Err("unsupported throws placement or nullability".into());
        }
        guard_type(t)?;
    }
    if (d.modifiers.len() > 1 && !(d.kind == "interface" && d.modifiers == ["open", "narrow"]))
        || d.modifiers.iter().any(|m| {
            !matches!(
                (d.kind.as_str(), m.as_str()),
                ("class", "open")
                    | ("interface", "open")
                    | ("interface", "narrow")
                    | ("fun", "static")
                    | ("property", "static")
            )
        })
    {
        return Err("unsupported modifier".into());
    }
    let needs_type = matches!(
        d.kind.as_str(),
        "field" | "const" | "property" | "typealias" | "lambda" | "exception"
    ) || (d.kind == "parameter" && parent != "field_constructor");
    let permits_type = needs_type || d.kind == "fun";
    if needs_type && d.ty.is_none() || !permits_type && d.ty.is_some() {
        return Err(format!("invalid type on {}", d.kind));
    }
    if let Some(t) = &mut d.ty {
        guard_type(t)?;
    }
    if !matches!(
        d.kind.as_str(),
        "fun" | "constructor" | "field_constructor" | "lambda"
    ) && !d.params.is_empty()
    {
        return Err("unexpected parameters".into());
    }
    if !matches!(
        d.kind.as_str(),
        "class" | "interface" | "struct" | "enum" | "property"
    ) && !d.children.is_empty()
    {
        return Err("unexpected child declarations".into());
    }
    if d.kind == "property"
        && !(d.children.is_empty()
            || d.children.len() <= 2
                && d.children[0].name == "get"
                && (d.children.len() == 1 || d.children[1].name == "set"))
    {
        return Err("invalid property accessors".into());
    }
    if d.kind == "accessor" && !["get", "set"].contains(&d.name.as_str()) {
        return Err("invalid accessor".into());
    }
    if d.kind == "field_constructor" && d.name != "constructor" {
        return Err("invalid field constructor".into());
    }
    if d.kind == "const" && d.literal.is_none() {
        return Err("constant requires a value".into());
    }
    if !matches!(d.kind.as_str(), "const" | "field" | "enumerator")
        && (d.literal.is_some() || d.value.is_some())
    {
        return Err("unexpected literal".into());
    }
    match (&d.value, &d.literal) {
        (None, None) => (),
        (Some(v), Some(l))
            if v == &l.raw
                && l.name.is_none()
                && matches!(
                    l.kind.as_str(),
                    "number"
                        | "boolean"
                        | "string"
                        | "null"
                        | "reference"
                        | "positional_enumerator"
                        | "struct"
                        | "list"
                        | "map"
                ) => {}
        _ => return Err("invalid or unsupported literal".into()),
    }
    if let Some(l) = &d.literal {
        let source = format!(
            "package verify\nstruct Example {{\nvalue: Int = {}\n}}\n",
            l.raw
        );
        let parsed =
            crate::parse("<literal>", &source, false).map_err(|_| "invalid literal source")?;
        let actual = parsed.declarations[0].children[0]
            .literal
            .as_ref()
            .ok_or("missing literal")?;
        fn same_literal(a: &crate::Literal, b: &crate::Literal) -> bool {
            a.kind == b.kind
                && a.raw == b.raw
                && a.name == b.name
                && a.children.len() == b.children.len()
                && a.children
                    .iter()
                    .zip(&b.children)
                    .all(|(a, b)| same_literal(a, b))
        }
        if !same_literal(actual, l) {
            return Err("inconsistent literal source".into());
        }
    }
    for p in &mut d.params {
        guard_decl(p, &d.kind)?;
    }
    for c in &mut d.children {
        guard_decl(c, &d.kind)?;
    }
    Ok(())
}

fn check_literal_types(model: &Model) -> Result<(), String> {
    fn aliases<'a>(decls: &'a [Decl], scope: &str, out: &mut BTreeMap<String, &'a TypeRef>) {
        for d in decls {
            let name = format!("{scope}.{}", d.name);
            if d.kind == "typealias" {
                out.insert(name.clone(), d.ty.as_ref().unwrap());
            }
            aliases(&d.children, &name, out);
        }
    }
    fn visit(decls: &[Decl], aliases: &BTreeMap<String, &TypeRef>) -> Result<(), String> {
        for d in decls {
            if let Some(l) = &d.literal {
                if d.kind != "enumerator" {
                    let mut ty = d.ty.as_ref().ok_or("literal has no type")?;
                    let mut nullable = ty.nullable;
                    let mut visited = BTreeSet::new();
                    while let Some(next) = ty.resolved.as_ref().and_then(|r| aliases.get(r)) {
                        if !visited.insert(ty.resolved.clone()) {
                            return Err("cyclic literal alias".into());
                        }
                        ty = next;
                        nullable |= ty.nullable;
                    }
                    let expected = match ty.name.as_str() {
                        "Boolean" => Some("boolean"),
                        "String" | "Date" | "Locale" => Some("string"),
                        "Byte" | "Short" | "Int" | "Long" | "UByte" | "UShort" | "UInt"
                        | "ULong" | "Float" | "Double" | "Duration" => Some("number"),
                        _ => None,
                    };
                    if expected.is_some_and(|e| {
                        l.kind != e && l.kind != "reference" && !(l.kind == "null" && nullable)
                    }) {
                        return Err("literal does not match its type".into());
                    }
                }
            }
            visit(&d.params, aliases)?;
            visit(&d.children, aliases)?;
        }
        Ok(())
    }
    let mut map = BTreeMap::new();
    for f in &model.files {
        aliases(&f.declarations, &f.package, &mut map);
    }
    for f in &model.files {
        visit(&f.declarations, &map)?;
    }
    Ok(())
}

struct Builder {
    nodes: Vec<Value>,
    refs: BTreeMap<String, Value>,
    raw: Map<String, Value>,
    overlays: Map<String, Value>,
    absences: Map<String, Value>,
    empty_path: Value,
    placeholders: Map<String, Value>,
    declarations: BTreeMap<String, Decl>,
    imports: Vec<String>,
    current_file: String,
    decl_paths: BTreeMap<(String, usize), (String, String)>,
}
impl Builder {
    fn new() -> Self {
        Self {
            nodes: vec![],
            refs: BTreeMap::new(),
            raw: Map::new(),
            overlays: Map::new(),
            absences: Map::new(),
            empty_path: Value::Null,
            placeholders: Map::new(),
            declarations: BTreeMap::new(),
            imports: Vec::new(),
            current_file: String::new(),
            decl_paths: BTreeMap::new(),
        }
    }
    fn reserve(&mut self, class: &str) -> Value {
        let id = format!("n{}", self.nodes.len() + 1);
        self.nodes.push(json!({"id":id,"class":format!("com.here.gluecodium.model.lime.{class}"),"properties":{}}));
        json!({"$ref":id})
    }
    fn set(&mut self, v: &Value, props: Value) {
        let id = v["$ref"].as_str().unwrap();
        let i = id[1..].parse::<usize>().unwrap() - 1;
        self.nodes[i]["properties"] = props;
    }
    fn node(&mut self, class: &str, props: Value) -> Value {
        let v = self.reserve(class);
        self.set(&v, props);
        v
    }
    fn path(&mut self, head: &[String], tail: &[String], suffix: &str) -> Value {
        self.node(
            "LimePath",
            json!({"head":head,"tail":tail,"disambiguator":suffix}),
        )
    }
    fn attr(&mut self, d: Option<&Decl>) -> Result<Value, String> {
        self.attributes(d.map(|d| d.annotations.as_slice()).unwrap_or(&[]))
    }
    fn attributes(&mut self, annotations: &[crate::Annotation]) -> Result<Value, String> {
        let attrs = annotation_map(annotations)?;
        Ok(self.node("LimeAttributes", json!({"attributes":attrs})))
    }
    fn decl_attributes(
        &mut self,
        d: &Decl,
        head: &[String],
        names: &[String],
    ) -> Result<Value, String> {
        let mut attrs = annotation_map(&d.annotations)?;
        if let Some(message) = attrs
            .get("DEPRECATED")
            .and_then(|v| v.get("MESSAGE"))
            .and_then(Value::as_str)
            .map(str::to_owned)
        {
            let parsed = docs::parse_text(&message)?;
            let mut path = names.to_vec();
            path.push("@deprecated".into());
            let path = self.path(head, &path, "");
            let comment = self.comment_data(&path, &parsed.description);
            attrs.get_mut("DEPRECATED").unwrap()["MESSAGE"] = comment;
        }
        Ok(self.node("LimeAttributes", json!({"attributes":attrs})))
    }
    fn accessor_attributes(
        &mut self,
        accessor: Option<&Decl>,
        parent: &Value,
        head: &[String],
        names: &[String],
    ) -> Result<Value, String> {
        let attrs = if let Some(d) = accessor {
            self.decl_attributes(d, head, names)?
        } else {
            self.attr(None)?
        };
        let index = |v: &Value| v["$ref"].as_str().unwrap()[1..].parse::<usize>().unwrap() - 1;
        let source = self.nodes[index(parent)]["properties"]["attributes"].clone();
        let target = self.nodes[index(&attrs)]["properties"]["attributes"]
            .as_object_mut()
            .unwrap();
        if let Some(message) = source.get("DEPRECATED").and_then(|v| v.get("MESSAGE")) {
            let group = target.entry("DEPRECATED").or_insert_with(|| json!({}));
            group
                .as_object_mut()
                .unwrap()
                .entry("MESSAGE")
                .or_insert_with(|| message.clone());
        }
        if source.get("INTERNAL").is_some() {
            target.entry("INTERNAL").or_insert_with(|| json!({}));
        }
        for platform in ["JAVA", "SWIFT", "DART", "KOTLIN"] {
            for key in ["INTERNAL", "PUBLIC"] {
                if let Some(value) = source.get(platform).and_then(|v| v.get(key)) {
                    target
                        .entry(platform)
                        .or_insert_with(|| json!({}))
                        .as_object_mut()
                        .unwrap()
                        .entry(key)
                        .or_insert_with(|| value.clone());
                }
            }
        }
        Ok(attrs)
    }
    fn external(&mut self, descriptor: Option<&crate::Descriptor>) -> Result<Value, String> {
        let Some(descriptor) = descriptor else {
            return Ok(Value::Null);
        };
        let mut result: BTreeMap<String, BTreeMap<String, String>> = BTreeMap::new();
        for entry in &descriptor.values {
            let value = crate::decode_lime_string(&entry.value)
                .map_err(|_| "invalid external descriptor string")?;
            result
                .entry(entry.platform.to_ascii_lowercase())
                .or_default()
                .insert(entry.key.to_ascii_lowercase(), value);
        }
        Ok(self.node("LimeExternalDescriptor", json!({"descriptors":result})))
    }
    fn comment(&mut self, path: &Value) -> Value {
        let v = self.node(
            "LimeComment",
            json!({"isExcluded":false,"path":path,"placeholders":self.placeholders}),
        );
        self.raw
            .insert(v["$ref"].as_str().unwrap().into(), json!([]));
        v
    }
    fn comment_data(&mut self, path: &Value, data: &docs::Comment) -> Value {
        let value = self.comment(path);
        self.update_comment(&value, path, data);
        value
    }
    fn update_comment(&mut self, value: &Value, path: &Value, data: &docs::Comment) {
        let id = value["$ref"].as_str().unwrap();
        let index = id[1..].parse::<usize>().unwrap() - 1;
        self.nodes[index]["properties"]["path"] = path.clone();
        self.nodes[index]["properties"]["isExcluded"] = json!(data.is_excluded);
        self.raw.insert(id.into(), json!(data.sections));
    }
    fn empty_comment(&mut self) -> Value {
        let p = self.empty_path.clone();
        self.comment(&p)
    }
    fn basic(&mut self) -> Result<(), String> {
        for (name, _) in BASIC {
            let v = self.reserve("LimeBasicType");
            self.refs.insert((*name).into(), v);
        }
        for (name, id) in BASIC {
            let v = self.refs[*name].clone();
            let a = self.attr(None)?;
            let c = self.empty_comment();
            let child = if *name == "Blob" {
                vec![self.basic_ref("UByte", false)?]
            } else {
                vec![]
            };
            self.set(&v,json!({"attributes":a,"childTypes":child,"comment":c,"external":null,"path":self.empty_path,"typeId":{"enum":"com.here.gluecodium.model.lime.LimeBasicType$TypeId","name":id}}));
            self.overlays.insert(
                v["$ref"].as_str().unwrap().into(),
                json!({"name":name,"fullName":name,"actualType":v}),
            );
        }
        Ok(())
    }
    fn basic_ref(&mut self, name: &str, nullable: bool) -> Result<Value, String> {
        let target = self.refs.get(name).ok_or("missing basic type")?.clone();
        let a = self.attr(None)?;
        let id = BASIC.iter().find(|(n, _)| *n == name).unwrap().1;
        Ok(self.node("LimeBasicTypeRef",json!({"attributes":a,"element":target,"elementFullName":id,"isNullable":nullable,"type":target})))
    }
    fn type_ref(&mut self, t: &TypeRef) -> Result<Value, String> {
        if BASIC.iter().any(|(n, _)| *n == t.name) {
            let r = self.basic_ref(&t.name, t.nullable)?;
            let a = self.attributes(&t.annotations)?;
            let i = r["$ref"].as_str().unwrap()[1..].parse::<usize>().unwrap() - 1;
            self.nodes[i]["properties"]["attributes"] = a;
            return Ok(r);
        }
        let target = if t.builtin {
            let args = t
                .args
                .iter()
                .map(|a| self.type_ref(a))
                .collect::<Result<Vec<_>, _>>()?;
            let attr = self.attr(None)?;
            let comment = self.empty_comment();
            let mut p = json!({"attributes":attr,"childTypes":args,"comment":comment,"external":null,"path":self.empty_path});
            if t.name == "Map" {
                p["keyType"] = args[0].clone();
                p["valueType"] = args[1].clone();
            } else {
                p["elementType"] = args[0].clone();
            }
            let v = self.node(&format!("Lime{}", t.name), p);
            self.overlays
                .insert(v["$ref"].as_str().unwrap().into(), json!({"actualType":v}));
            v
        } else {
            self.refs
                .get(t.resolved.as_ref().ok_or("unresolved type")?)
                .ok_or("missing resolved type")?
                .clone()
        };
        let a = self.attributes(&t.annotations)?;
        let kind = if t.builtin {
            "LimeDirectTypeRef"
        } else {
            "LimeAmbiguousTypeRef"
        };
        Ok(self.node(
            kind,
            json!({"attributes":a,"element":target,"isNullable":t.nullable,"type":target}),
        ))
    }
    fn alloc(
        &mut self,
        d: &Decl,
        head: &[String],
        tail: &[String],
        field_index: &mut usize,
        inherited_suffix: Option<&str>,
    ) -> Result<(), String> {
        let mut path = tail.to_vec();
        path.push(if d.kind == "field_constructor" {
            String::new()
        } else {
            d.name.clone()
        });
        let base = head
            .iter()
            .chain(&path)
            .cloned()
            .collect::<Vec<_>>()
            .join(".");
        let suffix = if d.kind == "field_constructor" {
            let i = *field_index;
            *field_index += 1;
            i.to_string()
        } else if let Some(suffix) = inherited_suffix {
            suffix.to_owned()
        } else if self.refs.contains_key(&base) {
            let mut i = 1;
            while self.refs.contains_key(&format!("{base}:{i}")) {
                i += 1;
            }
            i.to_string()
        } else {
            String::new()
        };
        let full = if suffix.is_empty() {
            base
        } else {
            format!("{base}:{suffix}")
        };
        self.decl_paths.insert(
            (self.current_file.clone(), d.span.start),
            (full.clone(), suffix.clone()),
        );
        let class = match d.kind.as_str() {
            "class" => "LimeClass",
            "interface" => "LimeInterface",
            "struct" => "LimeStruct",
            "enum" => "LimeEnumeration",
            "exception" => "LimeException",
            "typealias" => "LimeTypeAlias",
            "lambda" => "LimeLambda",
            "fun" | "constructor" => "LimeFunction",
            "property" => "LimeProperty",
            "field" => "LimeField",
            "const" => "LimeConstant",
            "enumerator" => "LimeEnumerator",
            "field_constructor" => "LimeFieldConstructor",
            "parameter" => "LimeParameter",
            _ => return Err("invalid declaration".into()),
        };
        let v = self.reserve(class);
        if self.refs.insert(full.clone(), v).is_some() {
            return Err(format!("duplicate declaration {full}"));
        }
        let mut nested_index = 0;
        for c in &d.children {
            if c.kind != "accessor" {
                self.alloc(c, head, &path, &mut nested_index, None)?;
            }
        }
        for (i, p) in d.params.iter().enumerate() {
            if d.kind != "field_constructor" {
                let mut p = p.clone();
                if d.kind == "lambda" && p.name.is_empty() {
                    p.name = format!("p{i}");
                }
                self.alloc(&p, head, &path, &mut nested_index, Some(&suffix))?;
            }
        }
        Ok(())
    }
    fn return_type(&mut self, ty: Value, comment_path: &Value) -> Result<Value, String> {
        let a = self.attr(None)?;
        let c = self.comment(comment_path);
        Ok(self.node(
            "LimeReturnType",
            json!({"attributes":a,"comment":c,"typeRef":ty}),
        ))
    }
    fn function(
        &mut self,
        path: Value,
        comment_path: &Value,
        ty: Value,
        params: Vec<Value>,
        is_static: bool,
        is_constructor: bool,
    ) -> Result<Value, String> {
        let a = self.attr(None)?;
        let c = self.comment(comment_path);
        let return_path = if params.is_empty() {
            comment_path.clone()
        } else {
            self.empty_path.clone()
        };
        let ret = self.return_type(ty, &return_path)?;
        Ok(self.node("LimeFunction",json!({"attributes":a,"comment":c,"external":null,"isConstructor":is_constructor,"isStatic":is_static,"parameters":params,"path":path,"returnType":ret,"thrownType":null})))
    }
    fn find_value_target(&self, name: &str, scope: &str) -> Result<String, String> {
        let mut candidates = BTreeSet::new();
        for import in &self.imports {
            let short = import.rsplit('.').next().unwrap_or(import);
            if name == short || name.starts_with(&format!("{short}.")) {
                let full = format!("{}{}", import, &name[short.len()..]);
                if self.declarations.contains_key(&full) {
                    candidates.insert(full);
                }
            }
        }
        let mut here = scope;
        loop {
            let full = if here.is_empty() {
                name.to_owned()
            } else {
                format!("{here}.{name}")
            };
            if self.declarations.contains_key(&full) {
                candidates.insert(full);
            }
            match here.rsplit_once('.') {
                Some((p, _)) => here = p,
                None if !here.is_empty() => here = "",
                None => break,
            }
        }
        if candidates.len() == 1 {
            Ok(candidates.into_iter().next().unwrap())
        } else {
            Err(format!("unresolved or ambiguous value reference {name}"))
        }
    }
    fn actual_source_type(&self, ty: &TypeRef) -> Result<TypeRef, String> {
        let mut ty = ty.clone();
        let mut seen = BTreeSet::new();
        while let Some(name) = ty.resolved.clone() {
            let Some(decl) = self.declarations.get(&name) else {
                break;
            };
            if decl.kind != "typealias" {
                break;
            }
            if !seen.insert(name) {
                return Err("cyclic alias".into());
            }
            ty = decl.ty.clone().ok_or("missing alias type")?;
        }
        Ok(ty)
    }
    fn literal(
        &mut self,
        l: &crate::Literal,
        ty: &Value,
        source_ty: Option<&TypeRef>,
        scope: &str,
    ) -> Result<Value, String> {
        let a = self.attr(None)?;
        match l.kind.as_str() {
            "null" => return Ok(self.node("LimeValue$Null", json!({"attributes":a,"typeRef":ty}))),
            "reference" | "positional_enumerator" => {
                let (name, position) = if l.kind == "positional_enumerator" {
                    let (n, npos) = l
                        .raw
                        .split_once('(')
                        .ok_or("invalid positional enumerator")?;
                    let index: i64 = npos
                        .trim_end_matches(')')
                        .replace('_', "")
                        .parse()
                        .map_err(|_| "invalid positional enumerator")?;
                    (n.trim(), Some(index))
                } else {
                    (l.raw.trim(), None)
                };
                let clean_name = name.replace('`', "");
                let mut target = self.find_value_target(&clean_name, scope)?;
                let reference = if let Some(index) = position {
                    let enum_decl = self
                        .declarations
                        .get(&target)
                        .ok_or("unknown enumeration")?
                        .clone();
                    if enum_decl.kind != "enum" {
                        return Err("positional value requires an enumeration".into());
                    }
                    let mut next = 0i32;
                    let mut found = None;
                    for item in enum_decl.children.iter().filter(|d| d.kind == "enumerator") {
                        if let Some(literal) = &item.literal {
                            if literal.kind != "number" {
                                next = 0;
                                continue;
                            }
                            let raw: String =
                                literal.raw.chars().filter(|c| !c.is_whitespace()).collect();
                            let raw = raw.strip_prefix('+').unwrap_or(&raw);
                            if raw == index.to_string() {
                                found = Some(item.name.clone());
                                break;
                            }
                            next = raw
                                .parse::<i32>()
                                .ok()
                                .and_then(|n| n.checked_add(1))
                                .unwrap_or(0);
                        } else {
                            if i64::from(next) == index {
                                found = Some(item.name.clone());
                                break;
                            }
                            next = next.checked_add(1).unwrap_or(0);
                        }
                    }
                    target.push('.');
                    target.push_str(&found.ok_or("positional enumerator not found")?);
                    let element = self.refs.get(&target).ok_or("missing enumerator")?.clone();
                    let enum_target = target.rsplit_once('.').unwrap().0;
                    let enum_ref = self
                        .refs
                        .get(enum_target)
                        .ok_or("missing enumeration")?
                        .clone();
                    let attrs = self.attr(None)?;
                    let enum_type = self.node("LimeAmbiguousTypeRef",json!({"attributes":attrs,"element":enum_ref,"isNullable":false,"type":enum_ref}));
                    let attrs = self.attr(None)?;
                    self.node("LimePositionalEnumeratorRef",json!({"attributes":attrs,"element":element,"typeRef":enum_type,"index":index}))
                } else {
                    let element = self
                        .refs
                        .get(&target)
                        .ok_or("missing value target")?
                        .clone();
                    let decl = self
                        .declarations
                        .get(&target)
                        .ok_or("missing value declaration")?;
                    if !matches!(decl.kind.as_str(), "const" | "enumerator") {
                        return Err("reference must name a constant or enumerator".into());
                    }
                    let attrs = self.attr(None)?;
                    self.node(
                        "LimeAmbiguousConstantRef",
                        json!({"attributes":attrs,"element":element}),
                    )
                };
                return Ok(self.node(
                    "LimeValue$Constant",
                    json!({"attributes":a,"typeRef":ty,"valueRef":reference}),
                ));
            }
            "list" | "map" | "struct" => {
                let source = self.actual_source_type(source_ty.ok_or("initializer lacks type")?)?;
                let mut values = Vec::new();
                if l.kind == "struct" {
                    let decl = self
                        .declarations
                        .get(
                            source
                                .resolved
                                .as_ref()
                                .ok_or("struct initializer needs struct type")?,
                        )
                        .ok_or("unknown struct")?
                        .clone();
                    let fields: Vec<_> =
                        decl.children.iter().filter(|f| f.kind == "field").collect();
                    for (i, item) in l.children.iter().enumerate() {
                        let field = if let Some(name) = &item.name {
                            fields.iter().find(|f| &f.name == name).copied()
                        } else {
                            fields.get(i).copied()
                        }
                        .ok_or("too many struct initializer values")?;
                        let field_ty = field.ty.as_ref().ok_or("field lacks type")?;
                        let graph_ty = self.type_ref(field_ty)?;
                        values.push(self.literal(item, &graph_ty, Some(field_ty), scope)?);
                    }
                } else {
                    let types = if source.name == "Blob" {
                        vec![TypeRef {
                            name: "UByte".into(),
                            builtin: true,
                            args: vec![],
                            nullable: false,
                            docs: vec![],
                            annotations: vec![],
                            span: source.span.clone(),
                            resolved: None,
                        }]
                    } else {
                        source.args.clone()
                    };
                    if l.kind == "map" {
                        if types.len() != 2 {
                            return Err("map initializer requires a map type".into());
                        }
                        for pair in l.children.chunks_exact(2) {
                            let kt = self.type_ref(&types[0])?;
                            let vt = self.type_ref(&types[1])?;
                            let key = self.literal(&pair[0], &kt, Some(&types[0]), scope)?;
                            let value = self.literal(&pair[1], &vt, Some(&types[1]), scope)?;
                            let attrs = self.attr(None)?;
                            let void = self.basic_ref("Void", false)?;
                            values.push(self.node(
                                "LimeValue$KeyValuePair",
                                json!({"attributes":attrs,"typeRef":void,"key":key,"value":value}),
                            ));
                        }
                    } else {
                        if !l.children.is_empty() && types.is_empty() {
                            return Err("list initializer requires a collection type".into());
                        }
                        for item in &l.children {
                            let child = &types[0];
                            let graph_ty = self.type_ref(child)?;
                            values.push(self.literal(item, &graph_ty, Some(child), scope)?);
                        }
                    }
                }
                let kind = if l.kind == "struct" {
                    "LimeValue$StructInitializer"
                } else {
                    "LimeValue$InitializerList"
                };
                return Ok(self.node(kind, json!({"attributes":a,"typeRef":ty,"values":values})));
            }
            _ => (),
        }
        let normalized_number = if l.kind == "number" {
            l.raw
                .chars()
                .filter(|c| !c.is_whitespace())
                .collect::<String>()
        } else {
            String::new()
        };
        let raw = if l.kind == "number" {
            normalized_number.as_str()
        } else {
            l.raw.trim()
        };
        if ["NaN", "Infinity", "+Infinity", "-Infinity"].contains(&raw) {
            let name = match raw {
                "NaN" => "NAN",
                "-Infinity" => "NEGATIVE_INFINITY",
                _ => "INFINITY",
            };
            return Ok(self.node("LimeValue$Special",json!({"attributes":a,"typeRef":ty,"value":{"enum":"com.here.gluecodium.model.lime.LimeValue$Special$ValueId","name":name}})));
        }
        if l.kind == "number" {
            for (suffix, unit) in [
                ("min", "MINUTE"),
                ("ms", "MILLISECOND"),
                ("us", "MICROSECOND"),
                ("ns", "NANOSECOND"),
                ("d", "DAY"),
                ("h", "HOUR"),
                ("s", "SECOND"),
            ] {
                if let Some(value) = raw.strip_suffix(suffix) {
                    return Ok(self.node("LimeValue$Duration",json!({"attributes":a,"typeRef":ty,"value":value,"timeUnit":{"enum":"com.here.gluecodium.model.lime.LimeValue$Duration$TimeUnit","name":unit}})));
                }
            }
        }
        let value = match l.kind.as_str() {
            "string" => crate::decode_lime_string(&l.raw)?,
            "boolean" => l.raw.clone(),
            "number" => raw.strip_prefix('+').unwrap_or(raw).to_string(),
            _ => return Err("unsupported literal".into()),
        };
        Ok(self.node(
            "LimeValue$Literal",
            json!({"attributes":a,"typeRef":ty,"value":value}),
        ))
    }
    fn populate(
        &mut self,
        d: &Decl,
        head: &[String],
        tail: &[String],
        field_index: &mut usize,
    ) -> Result<(), String> {
        let mut names = tail.to_vec();
        names.push(if d.kind == "field_constructor" {
            String::new()
        } else {
            d.name.clone()
        });
        if d.kind == "field_constructor" {
            *field_index += 1;
        }
        let (key, suffix) = self
            .decl_paths
            .get(&(self.current_file.clone(), d.span.start))
            .cloned()
            .ok_or("missing declaration path")?;
        let v = self
            .refs
            .get(&key)
            .ok_or_else(|| format!("missing indexed declaration {key}"))?
            .clone();
        let path = self.path(head, &names, &suffix);
        let attr = self.decl_attributes(d, head, &names)?;
        let doc = docs::parse_documentation(&d.docs)?;
        let comment = self.comment_data(&path, &doc.description);
        let static_ = d.modifiers.iter().any(|m| m == "static");
        let mut groups: BTreeMap<&str, Vec<Value>> = BTreeMap::new();
        let mut next = 0;
        for c in &d.children {
            if c.kind == "accessor" {
                continue;
            }
            self.populate(c, head, &names, &mut next)?;
            let k = self
                .decl_paths
                .get(&(self.current_file.clone(), c.span.start))
                .ok_or("missing child path")?
                .0
                .clone();
            let group = match c.kind.as_str() {
                "class" => "classes",
                "interface" => "interfaces",
                "struct" => "structs",
                "enum" => "enumerations",
                "exception" => "exceptions",
                "typealias" => "typeAliases",
                "lambda" => "lambdas",
                "fun" | "constructor" => "functions",
                "property" => "properties",
                "field" => "fields",
                "const" => "constants",
                "enumerator" => "enumerators",
                "field_constructor" => "fieldConstructors",
                _ => return Err("unsupported member".into()),
            };
            groups.entry(group).or_default().push(self.refs[&k].clone());
        }
        let mut params = Vec::new();
        for (i, p) in d.params.iter().enumerate() {
            if d.kind == "field_constructor" {
                continue;
            }
            let mut p = p.clone();
            if d.kind == "lambda" && p.name.is_empty() {
                p.name = format!("p{i}");
            }
            self.populate(&p, head, &names, &mut 0)?;
            let k = self
                .decl_paths
                .get(&(self.current_file.clone(), p.span.start))
                .ok_or("missing parameter path")?
                .0
                .clone();
            let pv = self.refs[&k].clone();
            if d.kind == "lambda" {
                let idx = pv["$ref"].as_str().unwrap()[1..].parse::<usize>().unwrap() - 1;
                self.nodes[idx]["class"] =
                    json!("com.here.gluecodium.model.lime.LimeLambdaParameter");
                self.nodes[idx]["properties"]["isNamedParameter"] =
                    json!(!d.params[i].name.is_empty());
                let comment_id = self.nodes[idx]["properties"]["comment"]["$ref"]
                    .as_str()
                    .unwrap();
                let comment_index = comment_id[1..].parse::<usize>().unwrap() - 1;
                self.nodes[comment_index]["properties"]["path"] = path.clone();
            }
            if let Some(block) = doc
                .blocks
                .get(&("param".into(), p.name.clone()))
                .filter(|c| c.sections.iter().any(|(_, s)| !s.is_empty()))
            {
                if !p.docs.is_empty()
                    && docs::parse_documentation(&p.docs)?
                        .description
                        .sections
                        .iter()
                        .any(|(_, s)| !s.is_empty())
                {
                    return Err("redundant parameter documentation".into());
                }
                let comment = self.nodes
                    [pv["$ref"].as_str().unwrap()[1..].parse::<usize>().unwrap() - 1]["properties"]
                    ["comment"]
                    .clone();
                let mut block_path = names.clone();
                if d.kind != "lambda" {
                    block_path.push(p.name.clone());
                }
                let block_path = self.path(head, &block_path, "");
                self.update_comment(&comment, &block_path, block);
            }
            params.push(pv);
        }
        let external = self.external(d.descriptor.as_ref())?;
        let mut p = json!({"attributes":attr,"comment":comment,"external":external,"path":path});
        match d.kind.as_str() {
            "class" | "interface" | "struct" => {
                for group in [
                    "classes",
                    "interfaces",
                    "structs",
                    "enumerations",
                    "exceptions",
                    "typeAliases",
                    "lambdas",
                    "functions",
                    "properties",
                    "constants",
                ] {
                    p[group] = json!(groups.remove(group).unwrap_or_default());
                }
                p["childTypes"] = json!([]);
                if d.kind == "struct" {
                    let fields = groups.remove("fields").unwrap_or_default();
                    let children = fields
                        .iter()
                        .map(|f| {
                            let i = f["$ref"].as_str().unwrap()[1..].parse::<usize>().unwrap() - 1;
                            self.nodes[i]["properties"]["typeRef"].clone()
                        })
                        .collect::<Vec<_>>();
                    p["fields"] = json!(fields);
                    p["childTypes"] = json!(children);
                    p["fieldConstructors"] =
                        json!(groups.remove("fieldConstructors").unwrap_or_default());
                    p["constructorComment"] = if let Some(block) = doc
                        .blocks
                        .get(&("constructor".into(), String::new()))
                        .filter(|c| c.sections.iter().any(|(_, s)| !s.is_empty()))
                    {
                        self.comment_data(&path, block)
                    } else {
                        self.empty_comment()
                    };
                } else {
                    p["parents"] = json!(d
                        .parents
                        .iter()
                        .map(|p| self.type_ref(p))
                        .collect::<Result<Vec<_>, _>>()?);
                    p["isOpen"] =
                        json!(d.kind == "interface" || d.modifiers.iter().any(|m| m == "open"));
                    if d.kind == "interface" {
                        p["isNarrow"] = json!(d.modifiers.iter().any(|m| m == "narrow"));
                    }
                }
            }
            "enum" => {
                p["childTypes"] = json!([]);
                p["enumerators"] = json!(groups.remove("enumerators").unwrap_or_default());
            }
            "exception" => {
                p["childTypes"] = json!([]);
                p["errorType"] = self.type_ref(d.ty.as_ref().unwrap())?;
            }
            "typealias" => {
                p["childTypes"] = json!([]);
                p["typeRef"] = self.type_ref(d.ty.as_ref().unwrap())?;
            }
            "lambda" => {
                p["childTypes"] = json!([]);
                p["parameters"] = json!(params);
                let ty = self.type_ref(d.ty.as_ref().unwrap())?;
                p["returnType"] = self.return_type(ty, &path)?;
                if let Some(block) = doc
                    .blocks
                    .get(&("return".into(), String::new()))
                    .filter(|c| c.sections.iter().any(|(_, s)| !s.is_empty()))
                {
                    let mut parts = names.clone();
                    parts.push("@return".into());
                    let block_path = self.path(head, &parts, "");
                    let ret = &p["returnType"];
                    let i = ret["$ref"].as_str().unwrap()[1..].parse::<usize>().unwrap() - 1;
                    let c = self.nodes[i]["properties"]["comment"].clone();
                    self.update_comment(&c, &block_path, block);
                }
            }
            "fun" | "constructor" => {
                p["parameters"] = json!(params);
                p["isConstructor"] = json!(d.kind == "constructor");
                p["isStatic"] = json!(static_ || d.kind == "constructor");
                let ty = if d.kind == "constructor" {
                    let owner = head
                        .iter()
                        .chain(tail)
                        .cloned()
                        .collect::<Vec<_>>()
                        .join(".");
                    let target = self.refs[&owner].clone();
                    let a = self.attr(None)?;
                    self.node(
                        "LimeAmbiguousTypeRef",
                        json!({"attributes":a,"element":target,"isNullable":false,"type":target}),
                    )
                } else if let Some(t) = &d.ty {
                    self.type_ref(t)?
                } else {
                    self.basic_ref("Void", false)?
                };
                let return_path = if d.kind == "constructor" || d.ty.is_none() {
                    self.empty_path.clone()
                } else {
                    path.clone()
                };
                p["returnType"] = self.return_type(ty, &return_path)?;
                if !d.return_docs.is_empty() {
                    let own = docs::parse_documentation(&d.return_docs)?.description;
                    if doc
                        .blocks
                        .get(&("return".into(), String::new()))
                        .is_some_and(|b| b.sections.iter().any(|(_, s)| !s.is_empty()))
                        && own.sections.iter().any(|(_, s)| !s.is_empty())
                    {
                        return Err("redundant return documentation".into());
                    }
                    let i = p["returnType"]["$ref"].as_str().unwrap()[1..]
                        .parse::<usize>()
                        .unwrap()
                        - 1;
                    let c = self.nodes[i]["properties"]["comment"].clone();
                    self.update_comment(&c, &path, &own);
                }
                if let Some(block) = doc
                    .blocks
                    .get(&("return".into(), String::new()))
                    .filter(|c| c.sections.iter().any(|(_, s)| !s.is_empty()))
                {
                    let mut parts = names.clone();
                    parts.push("@return".into());
                    let block_path = self.path(head, &parts, "");
                    let ret = &p["returnType"];
                    let i = ret["$ref"].as_str().unwrap()[1..].parse::<usize>().unwrap() - 1;
                    let c = self.nodes[i]["properties"]["comment"].clone();
                    self.update_comment(&c, &block_path, block);
                }
                p["thrownType"] = if let Some(throws) = &d.throws {
                    let reference = self.type_ref(throws)?;
                    let own = docs::parse_documentation(&d.throws_docs)?.description;
                    let block = doc
                        .blocks
                        .get(&("throws".into(), String::new()))
                        .filter(|b| b.sections.iter().any(|(_, s)| !s.is_empty()));
                    if block.is_some() && own.sections.iter().any(|(_, s)| !s.is_empty()) {
                        return Err("redundant throws documentation".into());
                    }
                    let comment = if let Some(block) = block {
                        let mut parts = names.clone();
                        parts.push("@throws".into());
                        let block_path = self.path(head, &parts, "");
                        self.comment_data(&block_path, block)
                    } else {
                        self.comment_data(&path, &own)
                    };
                    self.node(
                        "LimeThrownType",
                        json!({"typeRef":reference,"comment":comment}),
                    )
                } else {
                    Value::Null
                };
            }
            "property" => {
                let ty = self.type_ref(d.ty.as_ref().unwrap())?;
                p["typeRef"] = ty.clone();
                p["isStatic"] = json!(static_);
                let value_comment = if let Some(value) = doc
                    .blocks
                    .get(&("value".into(), String::new()))
                    .filter(|c| c.sections.iter().any(|(_, s)| !s.is_empty()))
                {
                    if doc.description.sections.iter().any(|(_, s)| !s.is_empty()) {
                        return Err("redundant property value documentation".into());
                    }
                    let mut value = value.clone();
                    value.is_excluded = doc.description.is_excluded;
                    let mut parts = names.clone();
                    parts.push("@value".into());
                    let value_path = self.path(head, &parts, "");
                    self.comment_data(&value_path, &value)
                } else {
                    let empty = docs::Comment {
                        is_excluded: doc.description.is_excluded,
                        ..Default::default()
                    };
                    self.comment_data(&path, &empty)
                };
                let description_has_text =
                    doc.description.sections.iter().any(|(_, s)| !s.is_empty());
                let accessor_comment = if description_has_text {
                    comment.clone()
                } else {
                    value_comment.clone()
                };
                p["comment"] = accessor_comment.clone();
                p["valueComment"] = value_comment;
                p["additionalDescriptionComment"] = if let Some(block) = doc
                    .blocks
                    .get(&("description".into(), String::new()))
                    .filter(|c| c.sections.iter().any(|(_, s)| !s.is_empty()))
                {
                    let mut parts = names.clone();
                    parts.push("@description".into());
                    let bp = self.path(head, &parts, "");
                    let mut block = block.clone();
                    block.is_excluded = doc.description.is_excluded;
                    self.comment_data(&bp, &block)
                } else {
                    let empty = docs::Comment {
                        is_excluded: doc.description.is_excluded,
                        ..Default::default()
                    };
                    self.comment_data(&path, &empty)
                };
                let mut get_path = names.clone();
                get_path.push("get".into());
                let getp = self.path(head, &get_path, "");
                p["getter"] = self.function(getp, &path, ty.clone(), vec![], static_, false)?;
                let getter_index = p["getter"]["$ref"].as_str().unwrap()[1..]
                    .parse::<usize>()
                    .unwrap()
                    - 1;
                let getter = d.children.iter().find(|c| c.name == "get");
                let attributes =
                    self.accessor_attributes(getter, &p["attributes"], head, &names)?;
                self.nodes[getter_index]["properties"]["attributes"] = attributes;
                if let Some(accessor) = getter {
                    let external = self.external(accessor.descriptor.as_ref())?;
                    self.nodes[getter_index]["properties"]["external"] = external;
                }
                let ret = self.nodes[getter_index]["properties"]["returnType"].clone();
                let ret_index = ret["$ref"].as_str().unwrap()[1..].parse::<usize>().unwrap() - 1;
                self.nodes[ret_index]["properties"]["comment"] = accessor_comment.clone();
                let getter_comment = self.nodes[getter_index]["properties"]["comment"].clone();
                let mut getter_doc = doc
                    .blocks
                    .get(&("get".into(), String::new()))
                    .cloned()
                    .unwrap_or_default();
                let own_getter_doc = getter
                    .map(|a| docs::parse_documentation(&a.docs).map(|d| d.description))
                    .transpose()?
                    .unwrap_or_default();
                let own_getter_has_text =
                    own_getter_doc.sections.iter().any(|(_, s)| !s.is_empty());
                let block_getter_has_text = getter_doc.sections.iter().any(|(_, s)| !s.is_empty());
                if own_getter_has_text && block_getter_has_text {
                    return Err("redundant getter documentation".into());
                }
                if own_getter_has_text {
                    getter_doc = own_getter_doc;
                }
                getter_doc.is_excluded = doc.description.is_excluded;
                let getter_path = if block_getter_has_text {
                    let mut parts = names.clone();
                    parts.push("@get".into());
                    self.path(head, &parts, "")
                } else {
                    path.clone()
                };
                self.update_comment(&getter_comment, &getter_path, &getter_doc);
                if d.children.is_empty() || d.children.len() == 2 {
                    let mut param_path = get_path;
                    param_path.push("value".into());
                    let pp = self.path(head, &param_path, "");
                    let pa = self.attr(None)?;
                    let pc = accessor_comment.clone();
                    let param=self.node("LimeParameter",json!({"attributes":pa,"comment":pc,"external":null,"path":pp,"typeRef":ty}));
                    let mut set_path = names.clone();
                    set_path.push("set".into());
                    let sp = self.path(head, &set_path, "");
                    let void = self.basic_ref("Void", false)?;
                    p["setter"] = self.function(sp, &path, void, vec![param], static_, false)?;
                    let setter_index = p["setter"]["$ref"].as_str().unwrap()[1..]
                        .parse::<usize>()
                        .unwrap()
                        - 1;
                    let setter = d.children.iter().find(|c| c.name == "set");
                    let attributes =
                        self.accessor_attributes(setter, &p["attributes"], head, &names)?;
                    self.nodes[setter_index]["properties"]["attributes"] = attributes;
                    if let Some(accessor) = setter {
                        let external = self.external(accessor.descriptor.as_ref())?;
                        self.nodes[setter_index]["properties"]["external"] = external;
                    }
                    let setter_comment = self.nodes[setter_index]["properties"]["comment"].clone();
                    let mut setter_doc = doc
                        .blocks
                        .get(&("set".into(), String::new()))
                        .cloned()
                        .unwrap_or_default();
                    let own_setter_doc = setter
                        .map(|a| docs::parse_documentation(&a.docs).map(|d| d.description))
                        .transpose()?
                        .unwrap_or_default();
                    let own_setter_has_text =
                        own_setter_doc.sections.iter().any(|(_, s)| !s.is_empty());
                    let block_setter_has_text =
                        setter_doc.sections.iter().any(|(_, s)| !s.is_empty());
                    if own_setter_has_text && block_setter_has_text {
                        return Err("redundant setter documentation".into());
                    }
                    if own_setter_has_text {
                        setter_doc = own_setter_doc;
                    }
                    setter_doc.is_excluded = doc.description.is_excluded;
                    let setter_path = if block_setter_has_text {
                        let mut parts = names.clone();
                        parts.push("@set".into());
                        self.path(head, &parts, "")
                    } else {
                        path.clone()
                    };
                    self.update_comment(&setter_comment, &setter_path, &setter_doc);
                } else {
                    if doc.blocks.contains_key(&("set".into(), String::new())) {
                        return Err("setter documentation on readonly property".into());
                    }
                    p["setter"] = Value::Null;
                }
            }
            "parameter" => {
                p["typeRef"] = self.type_ref(d.ty.as_ref().ok_or("missing parameter type")?)?;
            }
            "field" | "const" => {
                let ty = self.type_ref(d.ty.as_ref().unwrap())?;
                p["typeRef"] = ty.clone();
                let value = if let Some(l) = &d.literal {
                    self.literal(l, &ty, d.ty.as_ref(), &key)?
                } else if d.kind == "field" && d.ty.as_ref().unwrap().nullable {
                    let a = self.attr(None)?;
                    self.node("LimeValue$Null", json!({"attributes":a,"typeRef":ty}))
                } else {
                    Value::Null
                };
                p[if d.kind == "field" {
                    "defaultValue"
                } else {
                    "value"
                }] = value;
            }
            "enumerator" => {
                let value = if let Some(l) = &d.literal {
                    let ty = self.basic_ref("Int", false)?;
                    self.literal(l, &ty, None, &key)?
                } else {
                    Value::Null
                };
                p["explicitValue"] = value;
            }
            "field_constructor" => {
                let owner = head
                    .iter()
                    .chain(tail)
                    .cloned()
                    .collect::<Vec<_>>()
                    .join(".");
                let target = self.refs[&owner].clone();
                let a = self.attr(None)?;
                p["structRef"]=self.node("LimeLazyTypeRef",json!({"attributes":a,"element":target,"elementFullName":owner,"isNullable":false,"type":target}));
                let mut fields = Vec::new();
                for param in &d.params {
                    let key = format!("{owner}.{}", param.name);
                    let f = self
                        .refs
                        .get(&key)
                        .ok_or("unknown field constructor field")?
                        .clone();
                    let a = self.attr(None)?;
                    fields.push(self.node("LimeLazyFieldRef", json!({"attributes":a,"element":f})));
                }
                p["fieldRefs"] = json!(fields);
            }
            _ => return Err("unsupported declaration".into()),
        }
        self.set(&v, p);
        Ok(())
    }
}

/// Adapt a native model to a validated compatibility-generation job.
/// Unsupported syntax is rejected before the backend is invoked.
pub fn build_job(model: &Model, options: &Options) -> Result<Value, String> {
    cpp_generation::validate_options(&serde_json::to_value(options).map_err(|e| e.to_string())?)?;
    let mut model = model.clone();
    if model.schema_version != 1 {
        return Err("unsupported native model schema".into());
    }
    if model.files.is_empty() || model.files.iter().all(|f| f.auxiliary) {
        return Err("at least one main file is required".into());
    }
    let mut paths = BTreeSet::new();
    for f in &mut model.files {
        if f.path.is_empty()
            || !paths.insert(f.path.clone())
            || !valid_qualified(&f.package)
            || f.imports.iter().any(|i| !valid_qualified(i))
            || f.declarations.is_empty()
        {
            return Err("invalid native file metadata".into());
        }
        validate_cpp_skip(&f.declarations)?;
        filter_declarations(&mut f.declarations, &options.tags, false)?;
        if options.strict {
            validate_strict(&f.declarations)?;
        }
        filter_declarations(&mut f.declarations, &options.tags, true)?;
        for d in &mut f.declarations {
            guard_decl(d, "file")?;
        }
    }
    crate::resolve_cpp(&mut model)?;
    fn collect_kinds(decls: &[Decl], scope: &str, kinds: &mut BTreeMap<String, String>) {
        for d in decls {
            let name = format!("{scope}.{}", d.name);
            kinds.insert(name.clone(), d.kind.clone());
            collect_kinds(&d.children, &name, kinds);
        }
    }
    fn check_value_type(ty: &TypeRef, kinds: &BTreeMap<String, String>) -> Result<(), String> {
        if ty
            .resolved
            .as_ref()
            .and_then(|s| kinds.get(s))
            .map(String::as_str)
            == Some("exception")
        {
            return Err("exception cannot be used as a value type".into());
        }
        for arg in &ty.args {
            check_value_type(arg, kinds)?;
        }
        Ok(())
    }
    fn check_exceptions(decls: &[Decl], kinds: &BTreeMap<String, String>) -> Result<(), String> {
        for d in decls {
            if d.kind != "exception" {
                if let Some(ty) = &d.ty {
                    check_value_type(ty, kinds)?;
                }
            }
            check_exceptions(&d.params, kinds)?;
            check_exceptions(&d.children, kinds)?;
        }
        Ok(())
    }
    let mut kinds = BTreeMap::new();
    for f in &model.files {
        collect_kinds(&f.declarations, &f.package, &mut kinds);
    }
    for f in &model.files {
        check_exceptions(&f.declarations, &kinds)?;
    }
    check_literal_types(&model)?;
    let mut b = Builder::new();
    fn index_decls(decls: &[Decl], scope: &str, out: &mut BTreeMap<String, Decl>) {
        for d in decls {
            let name = format!("{scope}.{}", d.name);
            out.insert(name.clone(), d.clone());
            index_decls(&d.children, &name, out);
        }
    }
    for f in &model.files {
        index_decls(&f.declarations, &f.package, &mut b.declarations);
    }
    let root = b.reserve("LimeModel");
    b.empty_path = b.path(&[], &[], "");
    for (name, source) in &options.docs_placeholders {
        let parsed = docs::parse_text(source)?;
        let path = b.empty_path.clone();
        let comment = b.comment_data(&path, &parsed.description);
        let i = comment["$ref"].as_str().unwrap()[1..]
            .parse::<usize>()
            .unwrap()
            - 1;
        b.nodes[i]["properties"]["placeholders"] = json!({});
        b.placeholders.insert(name.clone(), comment);
    }
    b.basic()?;
    for f in &model.files {
        let head = f.package.split('.').map(str::to_owned).collect::<Vec<_>>();
        b.current_file = f.path.clone();
        let mut index = 0;
        for d in &f.declarations {
            b.alloc(d, &head, &[], &mut index, None)?;
        }
    }
    let mut top = Vec::new();
    let mut aux = Vec::new();
    let mut files = BTreeMap::new();
    for f in &model.files {
        let head = f.package.split('.').map(str::to_owned).collect::<Vec<_>>();
        b.imports = f.imports.clone();
        b.current_file = f.path.clone();
        let mut index = 0;
        for d in &f.declarations {
            b.populate(d, &head, &[], &mut index)?;
            let key = b.decl_paths[&(f.path.clone(), d.span.start)].0.clone();
            let v = b.refs[&key].clone();
            if f.auxiliary {
                aux.push(v)
            } else {
                top.push(v)
            }
            files.insert(key, f.path.clone());
        }
    }
    let mut indexed = b.refs.clone();
    indexed.retain(|_, v| {
        let i = v["$ref"].as_str().unwrap()[1..].parse::<usize>().unwrap() - 1;
        !b.nodes[i]["class"]
            .as_str()
            .unwrap()
            .ends_with(".LimeLambdaParameter")
    });
    b.set(&root,json!({"auxiliaryElements":aux,"fileNameMap":files,"referenceMap":indexed,"topElements":top}));
    // Derive type views by chasing alias edges; all targets come from this graph.
    for i in 0..b.nodes.len() {
        let kind = b.nodes[i]["class"]
            .as_str()
            .unwrap()
            .rsplit('.')
            .next()
            .unwrap();
        if !matches!(
            kind,
            "LimeClass"
                | "LimeInterface"
                | "LimeStruct"
                | "LimeEnumeration"
                | "LimeException"
                | "LimeLambda"
                | "LimeTypeAlias"
        ) {
            continue;
        }
        let id = b.nodes[i]["id"].as_str().unwrap().to_string();
        let mut target = json!({"$ref":id});
        let mut seen = BTreeSet::new();
        loop {
            let n = target["$ref"].as_str().ok_or("invalid alias target")?;
            if !seen.insert(n.to_string()) {
                return Err("cyclic alias".into());
            }
            let j = n[1..].parse::<usize>().map_err(|_| "invalid node")? - 1;
            if !b.nodes[j]["class"]
                .as_str()
                .unwrap()
                .ends_with(".LimeTypeAlias")
            {
                break;
            }
            let r = b.nodes[j]["properties"]["typeRef"]["$ref"]
                .as_str()
                .ok_or("invalid alias reference")?;
            let k = r[1..].parse::<usize>().map_err(|_| "invalid reference")? - 1;
            target = b.nodes[k]["properties"]["type"].clone();
        }
        b.overlays.entry(id).or_insert_with(|| json!({}))["actualType"] = target;
    }
    // These are absent getter names on the admitted model classes. The backend
    // derives its computed views separately; a stored property always wins.
    let absence_names = [
        "propertyElement",
        "isVirtual",
        "isConst",
        "isAsyncHelper",
        "internalNamespace",
        "exportName",
        "functionUsings",
        "needsExport",
        "storageQualifier",
        "structElement",
        "struct",
        "iter",
        "constructorComment",
    ];
    let mut class_properties: BTreeMap<&str, BTreeSet<&str>> = BTreeMap::new();
    for node in &b.nodes {
        let class = node["class"].as_str().unwrap();
        class_properties.entry(class).or_default().extend(
            node["properties"]
                .as_object()
                .unwrap()
                .keys()
                .map(String::as_str),
        );
    }
    for n in &b.nodes {
        let kind = n["class"].as_str().unwrap().rsplit('.').next().unwrap();
        if matches!(
            kind,
            "LimeModel" | "LimePath" | "LimeAttributes" | "LimeComment"
        ) {
            continue;
        }
        let mut absent = Vec::new();
        for name in absence_names {
            if !class_properties[n["class"].as_str().unwrap()].contains(name)
                && !(kind == "LimeFieldConstructor" && name == "struct")
            {
                absent.push(name);
            }
        }
        b.absences
            .insert(n["id"].as_str().unwrap().into(), json!(absent));
    }
    Ok(
        json!({"schema":"gluecodium.cpp-generation-job","version":2,"snapshot":{"schema":"gluecodium.reference-model.snapshot","version":1,"root":root,"nodes":b.nodes},"raw_comments":b.raw,"property_overlays":b.overlays,"absent_properties":b.absences,"options":options}),
    )
}
/// Generate every file in memory using unchanged production templates.
pub fn generate(
    model: &Model,
    templates: impl AsRef<Path>,
    options: &Options,
) -> Result<Vec<cpp_generation::GeneratedFile>, String> {
    generate_with_diagnostics(model, templates, options).map(|(files, _)| files)
}

/// Generate all files and return any non-fatal rendering diagnostics.
pub fn generate_with_diagnostics(
    model: &Model,
    templates: impl AsRef<Path>,
    options: &Options,
) -> Result<(Vec<cpp_generation::GeneratedFile>, Vec<String>), String> {
    let job = build_job(model, options)?;
    cpp_generation::generate_with_diagnostics(templates, &job)
}
