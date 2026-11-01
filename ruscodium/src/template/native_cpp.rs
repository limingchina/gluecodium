//! Native, deliberately bounded C++ name resolution over reference snapshots.
use super::graph::{reference, Graph, ModelNode};
use serde_json::Value;
use std::collections::{BTreeMap, BTreeSet};

#[derive(Clone, Debug, Default)]
pub struct NativeCppConfig {
    pub root_namespace: Vec<String>,
    pub internal_namespace: Vec<String>,
    pub predicates: bool,
    pub sorters: bool,
}
impl NativeCppConfig {
    pub fn parse(value: &Value) -> Result<Self, String> {
        let object = value.as_object().ok_or("native_cpp must be an object")?;
        if let Some(key) = object.keys().find(|k| {
            ![
                "root_namespace",
                "internal_namespace",
                "predicates",
                "sorters",
            ]
            .contains(&k.as_str())
        }) {
            return Err(format!("unsupported native_cpp option {key}"));
        }
        let parse = |key: &str| -> Result<Vec<String>, String> {
            let Some(value) = object.get(key) else {
                return Ok(Vec::new());
            };
            value
                .as_array()
                .ok_or_else(|| format!("native_cpp.{key} must be an array"))?
                .iter()
                .map(|v| {
                    let s = v
                        .as_str()
                        .ok_or_else(|| format!("native_cpp.{key} components must be strings"))?;
                    let mut chars = s.bytes();
                    if !chars
                        .next()
                        .is_some_and(|c| c.is_ascii_alphabetic() || c == b'_')
                        || !chars.all(|c| c.is_ascii_alphanumeric() || c == b'_')
                    {
                        return Err(format!("invalid namespace component {s:?}"));
                    }
                    Ok(s.to_owned())
                })
                .collect()
        };
        Ok(Self {
            root_namespace: parse("root_namespace")?,
            internal_namespace: parse("internal_namespace")?,
            predicates: flag(object, "predicates")?,
            sorters: flag(object, "sorters")?,
        })
    }
}

fn flag(object: &serde_json::Map<String, Value>, key: &str) -> Result<bool, String> {
    object
        .get(key)
        .map(|v| {
            v.as_bool()
                .ok_or_else(|| format!("native_cpp.{key} must be a boolean"))
        })
        .transpose()
        .map(|v| v.unwrap_or(false))
}

#[derive(Clone, Debug, Eq, Ord, PartialEq, PartialOrd)]
struct ModelPath {
    head: Vec<String>,
    tail: Vec<String>,
    disambiguator: String,
}

/// Resolve a C++ name directly from graph facts. A null result represents an absent accessor.
pub fn resolve(
    graph: &Graph,
    config: &NativeCppConfig,
    selector: &str,
    mode: &str,
    receiver: &Value,
) -> Result<Option<String>, String> {
    NativeCppResolver::new(graph, config.clone())?.resolve(graph, selector, mode, receiver)
}

/// A resolver with an index of actual named nodes from one graph.
pub(super) struct NativeCppResolver {
    config: NativeCppConfig,
    parents: BTreeMap<ModelPath, Vec<String>>,
}
impl NativeCppResolver {
    pub(super) fn new(graph: &Graph, config: NativeCppConfig) -> Result<Self, String> {
        let mut parents: BTreeMap<ModelPath, Vec<String>> = BTreeMap::new();
        let empty = BTreeMap::new();
        let ctx = Resolver {
            graph,
            config: &config,
            parents: &empty,
        };
        for (id, node) in &graph.nodes {
            if node.properties.contains_key("attributes")
                && node.properties.contains_key("external")
                && node.properties.contains_key("path")
            {
                let value = serde_json::json!({"$ref": id});
                parents
                    .entry(ctx.path(&value)?)
                    .or_default()
                    .push(id.clone());
            }
        }
        Ok(Self { config, parents })
    }
    pub(super) fn resolve(
        &self,
        graph: &Graph,
        selector: &str,
        mode: &str,
        receiver: &Value,
    ) -> Result<Option<String>, String> {
        if !["", "C++", "FQN"].contains(&selector) {
            return Err(format!("unsupported native C++ resolver {selector}"));
        }
        if !["name", "getter", "setter", "ref"].contains(&mode) {
            return Err(format!("unsupported native C++ mode {mode}"));
        }
        if receiver.is_null() {
            return Ok(None);
        }
        if mode == "ref" {
            return Err("native C++ ref mode is unsupported".into());
        }
        let ctx = Resolver {
            graph,
            config: &self.config,
            parents: &self.parents,
        };
        if selector == "FQN" {
            if mode != "name" {
                return Err(format!("FQN {mode} mode is unsupported"));
            }
            let mut v = receiver.clone();
            if ctx.class(&v)? == "com.here.gluecodium.model.lime.LimeReturnType" {
                v = ctx.get(&v, "typeRef")?.clone();
            }
            if matches!(
                ctx.class(&v)?,
                "com.here.gluecodium.model.lime.LimeBasicTypeRef"
                    | "com.here.gluecodium.model.lime.LimeDirectTypeRef"
                    | "com.here.gluecodium.model.lime.LimeAmbiguousTypeRef"
            ) {
                v = ctx.get(&v, "type")?.clone();
            }
            return ctx.full_name(&v, &mut BTreeSet::new()).map(Some);
        }
        if mode != "name" {
            return ctx.accessor(receiver, mode);
        }
        ctx.name(receiver, &mut BTreeSet::new()).map(Some)
    }
}
struct Resolver<'a> {
    graph: &'a Graph,
    config: &'a NativeCppConfig,
    parents: &'a BTreeMap<ModelPath, Vec<String>>,
}
impl<'a> Resolver<'a> {
    fn node(&self, v: &Value) -> Result<&'a ModelNode, String> {
        let id = reference(v).ok_or("native C++ expected model reference")?;
        self.graph
            .nodes
            .get(id)
            .ok_or_else(|| format!("native C++ missing node {id}"))
    }
    fn class<'b>(&'b self, v: &'b Value) -> Result<&'b str, String> {
        let class = self
            .graph
            .class(v)
            .ok_or_else(|| "native C++ expected model class".to_string())?;
        let simple = class
            .strip_prefix("com.here.gluecodium.model.lime.")
            .ok_or_else(|| format!("unsupported native C++ model class {class}"))?;
        if simple.contains('.') {
            return Err(format!("unsupported native C++ model class {class}"));
        }
        Ok(class)
    }
    fn get(&self, v: &Value, key: &str) -> Result<&'a Value, String> {
        self.node(v)?.properties.get(key).ok_or_else(|| {
            format!(
                "native C++ missing {key} on {}",
                self.class(v).unwrap_or("node")
            )
        })
    }
    fn path(&self, v: &Value) -> Result<ModelPath, String> {
        let p = self.get(v, "path")?;
        let array = |key| -> Result<Vec<String>, String> {
            self.get(p, key)?
                .as_array()
                .ok_or_else(|| format!("invalid LimePath {key}"))?
                .iter()
                .map(|v| {
                    v.as_str()
                        .map(str::to_owned)
                        .ok_or_else(|| format!("invalid LimePath {key} component"))
                })
                .collect()
        };
        Ok(ModelPath {
            head: array("head")?,
            tail: array("tail")?,
            disambiguator: self
                .get(p, "disambiguator")?
                .as_str()
                .ok_or("invalid LimePath disambiguator")?
                .into(),
        })
    }
    fn attributes(&self, v: &Value) -> Result<&'a serde_json::Map<String, Value>, String> {
        let attrs = self.get(v, "attributes")?;
        self.get(attrs, "attributes")?
            .as_object()
            .ok_or_else(|| "invalid native C++ attributes".into())
    }
    fn attr<'b>(&'b self, v: &Value, group: &str, key: &str) -> Result<Option<&'b Value>, String> {
        let attrs = self.attributes(v)?;
        let Some(group_value) = attrs.get(group) else {
            return Ok(None);
        };
        let obj = group_value
            .as_object()
            .ok_or_else(|| format!("invalid {group} attribute"))?;
        Ok(obj.get(key))
    }
    fn checked(&self, v: &Value) -> Result<(), String> {
        let node = self.node(v)?;
        if node
            .properties
            .get("external")
            .is_some_and(|v| !v.is_null())
        {
            return Err("native C++ external descriptor unsupported".into());
        }
        if node.properties.contains_key("attributes") {
            let attrs = self.attributes(v)?;
            if let Some(cpp) = attrs.get("CPP") {
                let cpp = cpp.as_object().ok_or("invalid CPP attributes")?;
                if let Some(key) = cpp
                    .keys()
                    .find(|k| !["NAME", "TYPE", "ACCESSORS", "CONST"].contains(&k.as_str()))
                {
                    return Err(format!("unsupported C++ attribute {key}"));
                }
            }
        }
        Ok(())
    }
    fn parent(&self, v: &Value) -> Result<Option<Value>, String> {
        let mut path = self.path(v)?;
        if path.tail.len() <= 1 {
            return Ok(None);
        }
        path.tail.pop();
        path.disambiguator.clear();
        match self.parents.get(&path).map(Vec::as_slice) {
            Some([id]) => Ok(Some(serde_json::json!({"$ref": id}))),
            Some(_) => Err("duplicate native C++ parent path".into()),
            None => Err(format!(
                "native C++ missing parent context for {}",
                path.tail.join(".")
            )),
        }
    }
    fn short_name(&self, v: &Value) -> Result<String, String> {
        self.checked(v)?;
        let class = self.class(v)?.rsplit('.').next().unwrap_or("");
        if !matches!(
            class,
            "LimeField"
                | "LimeParameter"
                | "LimeFunction"
                | "LimeFieldConstructor"
                | "LimeConstant"
                | "LimeEnumerator"
                | "LimeEnumeration"
                | "LimeTypeAlias"
                | "LimeStruct"
                | "LimeClass"
                | "LimeInterface"
                | "LimeLambda"
                | "LimeProperty"
                | "LimeException"
        ) {
            return Err(format!("unsupported native C++ named element {class}"));
        }
        self.get(v, "external")?;
        if let Some(n) = self.attr(v, "CPP", "NAME")? {
            return n
                .as_str()
                .map(str::to_owned)
                .ok_or_else(|| "invalid C++ Name attribute".into());
        }
        let path = self.path(v)?;
        let n = path
            .tail
            .last()
            .ok_or("native C++ named element has empty path")?;
        match class {
            "LimeField" | "LimeParameter" | "LimeFunction" | "LimeFieldConstructor" => {
                snake(n, false)
            }
            "LimeConstant" | "LimeEnumerator" => snake(n, true),
            "LimeEnumeration" | "LimeTypeAlias" | "LimeStruct" | "LimeClass" | "LimeInterface"
            | "LimeLambda" => upper_camel(n),
            "LimeProperty" | "LimeException" => Err(format!(
                "native C++ default name rule unsupported for {class}"
            )),
            _ => Err(format!("unsupported native C++ named element {class}")),
        }
    }
    fn full_name(&self, v: &Value, active: &mut BTreeSet<String>) -> Result<String, String> {
        let id = reference(v)
            .ok_or("native C++ expected named node")?
            .to_owned();
        if !active.insert(id.clone()) {
            return Err("native C++ cyclic parent dependency".into());
        }
        if active.len() > 128 {
            return Err("native C++ parent depth limit exceeded".into());
        }
        let path = self.path(v)?;
        let short = self.short_name(v)?;
        let prefix = if let Some(parent) = self.parent(v)? {
            self.full_name(&parent, active)?
        } else {
            let mut pieces = self.config.root_namespace.clone();
            pieces.extend(path.head);
            format!("::{}", pieces.join("::"))
        };
        active.remove(&id);
        Ok(format!("{prefix}::{short}"))
    }
    fn actual(&self, value: &Value, active: &mut BTreeSet<String>) -> Result<Value, String> {
        let mut current = value.clone();
        while self.class(&current)? == "com.here.gluecodium.model.lime.LimeTypeAlias" {
            let id = reference(&current).ok_or("invalid alias")?.to_owned();
            if !active.insert(id) {
                return Err("native C++ cyclic alias dependency".into());
            }
            if active.len() > 128 {
                return Err("native C++ alias depth limit exceeded".into());
            }
            self.checked(&current)?;
            self.get(&current, "external")?;
            current = self.get(self.get(&current, "typeRef")?, "type")?.clone();
        }
        Ok(current)
    }
    fn type_ref(&self, v: &Value, active: &mut BTreeSet<String>) -> Result<String, String> {
        self.checked(v)?;
        let ty = self.get(v, "type")?;
        let actual = self.actual(ty, &mut BTreeSet::new())?;
        let is_pointer = self.is_pointer(&actual)?;
        let name = self.type_name(ty, true, Some(v), active)?;
        let nullable = self
            .get(v, "isNullable")?
            .as_bool()
            .ok_or("invalid type ref nullability")?;
        if nullable && !is_pointer {
            Ok(format!("{}< {name} >", self.internal("optional")))
        } else {
            Ok(name)
        }
    }
    fn internal(&self, name: &str) -> String {
        format!(
            "::{}",
            self.config
                .internal_namespace
                .iter()
                .map(String::as_str)
                .chain([name])
                .collect::<Vec<_>>()
                .join("::")
        )
    }
    fn is_pointer(&self, ty: &Value) -> Result<bool, String> {
        Ok(matches!(
            self.class(ty)?.rsplit('.').next(),
            Some("LimeClass" | "LimeInterface")
        ))
    }
    fn type_name(
        &self,
        v: &Value,
        full: bool,
        attrs: Option<&Value>,
        active: &mut BTreeSet<String>,
    ) -> Result<String, String> {
        self.checked(v)?;
        self.get(v, "external")?;
        let id = reference(v).ok_or("invalid type reference")?.to_owned();
        if !active.insert(id.clone()) {
            return Err("native C++ cyclic type dependency".into());
        }
        if active.len() > 128 {
            return Err("native C++ type depth limit exceeded".into());
        }
        let class = self.class(v)?.rsplit('.').next().unwrap_or("");
        let result = match class {
            "LimeBasicType" => self.basic(self.get(v, "typeId")?, attrs),
            "LimeException" => Ok("::std::error_code".into()),
            "LimeList" | "LimeSet" | "LimeMap" => self.generic(v, class, attrs, active),
            "LimeEnumeration" | "LimeTypeAlias" | "LimeStruct" | "LimeClass" | "LimeInterface"
            | "LimeLambda" => {
                if full {
                    let n = self.full_name(v, &mut BTreeSet::new())?;
                    let actual = self.actual(v, &mut BTreeSet::new())?;
                    if self.is_pointer(&actual)? {
                        Ok(format!("::std::shared_ptr< {n} >"))
                    } else {
                        Ok(n)
                    }
                } else {
                    self.full_name(v, &mut BTreeSet::new())?;
                    self.short_name(v)
                }
            }
            _ => Err(format!("unsupported native C++ type {class}")),
        };
        active.remove(&id);
        result
    }
    fn basic(&self, id: &Value, attrs: Option<&Value>) -> Result<String, String> {
        if id.get("enum").and_then(Value::as_str)
            != Some("com.here.gluecodium.model.lime.LimeBasicType$TypeId")
        {
            return Err("invalid basic type ID".into());
        }
        let name = id
            .get("name")
            .and_then(Value::as_str)
            .ok_or("invalid basic type ID")?;
        if ["STRING", "DATE", "DURATION"].contains(&name) {
            if let Some(v) = attrs {
                if let Some(t) = self.attr(v, "CPP", "TYPE")? {
                    return t
                        .as_str()
                        .map(str::to_owned)
                        .ok_or_else(|| "invalid C++ Type attribute".into());
                }
            }
        }
        Ok(match name {
            "VOID" => "void",
            "INT8" => "int8_t",
            "UINT8" => "uint8_t",
            "INT16" => "int16_t",
            "UINT16" => "uint16_t",
            "INT32" => "int32_t",
            "UINT32" => "uint32_t",
            "INT64" => "int64_t",
            "UINT64" => "uint64_t",
            "BOOLEAN" => "bool",
            "FLOAT" => "float",
            "DOUBLE" => "double",
            "STRING" => "::std::string",
            "BLOB" => "::std::shared_ptr< ::std::vector< uint8_t > >",
            "DATE" => "::std::chrono::system_clock::time_point",
            "DURATION" => "::std::chrono::seconds",
            "LOCALE" => return Ok(self.internal("Locale")),
            _ => return Err(format!("unsupported basic type {name}")),
        }
        .into())
    }
    fn generic(
        &self,
        v: &Value,
        class: &str,
        attrs: Option<&Value>,
        active: &mut BTreeSet<String>,
    ) -> Result<String, String> {
        let element = if class == "LimeMap" {
            self.get(v, "keyType")?
        } else {
            self.get(v, "elementType")?
        };
        let mut first = self.type_ref(element, active)?;
        if class == "LimeList" {
            let optimized = if let Some(a) = attrs {
                self.attributes(a)?.contains_key("OPTIMIZED")
            } else {
                false
            };
            let actual = self.actual(self.get(element, "type")?, &mut BTreeSet::new())?;
            if optimized && !self.is_pointer(&actual)? {
                first = format!("::std::shared_ptr< {first} >");
            }
            return Ok(format!("::std::vector< {first} >"));
        }
        let actual = self.actual(self.get(element, "type")?, &mut BTreeSet::new())?;
        let std_hash = if self.class(&actual)? == "com.here.gluecodium.model.lime.LimeBasicType" {
            self.get(&actual, "typeId")?
                .get("name")
                .and_then(Value::as_str)
                .is_some_and(|n| {
                    [
                        "INT8", "UINT8", "INT16", "UINT16", "INT32", "UINT32", "INT64", "UINT64",
                        "FLOAT", "DOUBLE", "BOOLEAN", "STRING",
                    ]
                    .contains(&n)
                })
        } else {
            false
        };
        let hash = if std_hash {
            String::new()
        } else {
            format!(", {}< {first} >", self.internal("hash"))
        };
        if class == "LimeSet" {
            Ok(format!("::std::unordered_set< {first}{hash} >"))
        } else {
            let value = self.type_ref(self.get(v, "valueType")?, active)?;
            Ok(format!("::std::unordered_map< {first}, {value}{hash} >"))
        }
    }
    fn name(&self, v: &Value, active: &mut BTreeSet<String>) -> Result<String, String> {
        let class = self.class(v)?.rsplit('.').next().unwrap_or("");
        if class == "LimeBasicType$TypeId" {
            return self.basic(v, None);
        }
        match class {
            "LimeComment" => {
                if self.node(v)?.properties.get("isEmpty") == Some(&Value::Bool(true)) {
                    Ok(String::new())
                } else {
                    Err("native C++ nonempty or unavailable comment unsupported".into())
                }
            }
            "LimeReturnType" => self.type_ref(self.get(v, "typeRef")?, active),
            "LimeBasicTypeRef" | "LimeDirectTypeRef" | "LimeAmbiguousTypeRef" => {
                self.type_ref(v, active)
            }
            "LimeValue$Literal" => {
                let tr = self.get(v, "typeRef")?;
                let actual = self.actual(self.get(tr, "type")?, &mut BTreeSet::new())?;
                self.checked(&actual)?;
                self.get(&actual, "external")?;
                let value = self
                    .get(v, "value")?
                    .as_str()
                    .ok_or("invalid literal value")?;
                if self.class(&actual)? != "com.here.gluecodium.model.lime.LimeBasicType" {
                    return Err("unsupported native C++ nonbasic literal".into());
                }
                self.basic(self.get(&actual, "typeId")?, None)?;
                let id = self
                    .get(&actual, "typeId")?
                    .get("name")
                    .and_then(Value::as_str)
                    .ok_or("invalid literal type")?;
                match id {
                    "DATE" | "LOCALE" | "DURATION" => {
                        Err(format!("unsupported native C++ {id} literal"))
                    }
                    "FLOAT" => Ok(format!("{value}f")),
                    "STRING" => Ok(format!(
                        "\"{}\"",
                        value
                            .replace('\\', "\\\\")
                            .replace('"', "\\\"")
                            .replace('\n', "\\n")
                            .replace('\r', "\\r")
                            .replace('\t', "\\t")
                            .replace('\u{8}', "\\b")
                    )),
                    _ => Ok(value.into()),
                }
            }
            "LimeValue$Constant" => self.full_name(
                self.get(self.get(v, "valueRef")?, "element")?,
                &mut BTreeSet::new(),
            ),
            c if c.starts_with("LimeValue$") => Err(format!("unsupported native C++ value {c}")),
            "LimeBasicType" | "LimeException" | "LimeList" | "LimeSet" | "LimeMap"
            | "LimeEnumeration" | "LimeTypeAlias" | "LimeStruct" | "LimeClass"
            | "LimeInterface" | "LimeLambda" => self.type_name(v, false, None, active),
            _ => {
                self.full_name(v, &mut BTreeSet::new())?;
                self.short_name(v)
            }
        }
    }
    fn accessor(&self, v: &Value, mode: &str) -> Result<Option<String>, String> {
        self.checked(v)?;
        self.get(v, "external")?;
        let class = self.class(v)?.rsplit('.').next().unwrap_or("");
        if class == "LimeField" {
            let parent = self.parent(v)?.ok_or("native C++ field missing parent")?;
            self.checked(&parent)?;
            self.get(&parent, "external")?;
            if matches!(
                self.attr(&parent, "CPP", "ACCESSORS")?,
                None | Some(Value::Null | Value::Bool(false))
            ) {
                return Ok(None);
            }
        } else if class == "LimeProperty" {
            self.parent(v)?
                .ok_or("native C++ property missing parent")?;
            let accessor = self.get(v, mode)?;
            if !accessor.is_null() {
                self.checked(accessor)?;
                self.get(accessor, "external")?;
                if let Some(name) = self.attr(accessor, "CPP", "NAME")? {
                    return name
                        .as_str()
                        .map(|s| Some(s.to_owned()))
                        .ok_or_else(|| "invalid C++ accessor Name".into());
                }
            }
        } else {
            return Err(format!("unsupported native C++ {mode} receiver {class}"));
        }
        let path = self.path(v)?;
        let name = path.tail.last().ok_or("missing accessor name")?;
        let prefix = if mode == "setter" {
            "set"
        } else {
            let actual = self.actual(
                self.get(self.get(v, "typeRef")?, "type")?,
                &mut BTreeSet::new(),
            )?;
            if self.class(&actual)? == "com.here.gluecodium.model.lime.LimeBasicType" {
                self.basic(self.get(&actual, "typeId")?, None)?;
            }
            if self.class(&actual)? == "com.here.gluecodium.model.lime.LimeBasicType"
                && self
                    .get(&actual, "typeId")?
                    .get("name")
                    .and_then(Value::as_str)
                    == Some("BOOLEAN")
            {
                "is"
            } else {
                "get"
            }
        };
        Ok(Some(format!("{prefix}_{}", snake(name, false)?)))
    }
}
fn snake(input: &str, upper: bool) -> Result<String, String> {
    if !input.is_ascii() {
        return Err("native C++ Unicode casing unsupported".into());
    }
    let mixed = input.bytes().any(|c| c.is_ascii_lowercase())
        && input.bytes().any(|c| c.is_ascii_uppercase());
    let mut s = String::new();
    if !input.contains('_') && mixed {
        for (i, c) in input.chars().enumerate() {
            if c.is_ascii_uppercase() && i > 0 {
                s.push('_');
            }
            s.push(c.to_ascii_lowercase());
        }
    } else {
        s = input.to_ascii_lowercase();
    }
    if upper {
        s.make_ascii_uppercase();
    }
    Ok(s)
}
fn upper_camel(input: &str) -> Result<String, String> {
    if !input.is_ascii() {
        return Err("native C++ Unicode casing unsupported".into());
    }
    let mixed = input.bytes().any(|c| c.is_ascii_lowercase())
        && input.bytes().any(|c| c.is_ascii_uppercase());
    if input.contains('_') {
        return Ok(input.split('_').map(capitalize).collect());
    }
    if mixed {
        let mut chars = input.chars();
        return Ok(chars
            .next()
            .map(|c| c.to_ascii_uppercase().to_string() + chars.as_str())
            .unwrap_or_default());
    }
    Ok(capitalize(input))
}
fn capitalize(input: &str) -> String {
    let mut chars = input.chars();
    chars
        .next()
        .map(|c| c.to_ascii_uppercase().to_string() + &chars.as_str().to_ascii_lowercase())
        .unwrap_or_default()
}
