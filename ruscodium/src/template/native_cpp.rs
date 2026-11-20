//! Native C++ name resolution over reference snapshots.
#[path = "native_cpp_rules.rs"]
mod rules;
pub use rules::parse_cpp_properties;
pub(crate) fn validate_cpp_name_rules(rules: &BTreeMap<String, String>) -> Result<(), String> {
    rules::validate(rules)
}
pub(crate) fn cpp_rule_name(
    rules: &BTreeMap<String, String>,
    category: &str,
    input: &str,
    boolean: bool,
) -> Result<String, String> {
    rules::name(rules, category, input, boolean)
}
use super::graph::{reference, Graph, ModelNode};
use serde_json::Value;
use std::cell::RefCell;
use std::collections::{BTreeMap, BTreeSet};

#[derive(Clone, Debug, Default)]
pub struct NativeCppConfig {
    pub root_namespace: Vec<String>,
    pub internal_namespace: Vec<String>,
    pub predicates: bool,
    pub sorters: bool,
    pub name_rules: BTreeMap<String, String>,
    pub werror_doc_links: bool,
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
                "name_rules",
                "werror_doc_links",
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
                    let mut chars = s.chars();
                    if !chars
                        .next()
                        .is_some_and(|c| c == '_' || unicode_ident::is_xid_start(c))
                        || !chars.all(|c| c == '_' || unicode_ident::is_xid_continue(c))
                    {
                        return Err(format!("invalid namespace component {s:?}"));
                    }
                    Ok(s.to_owned())
                })
                .collect()
        };
        let config = Self {
            root_namespace: parse("root_namespace")?,
            internal_namespace: parse("internal_namespace")?,
            predicates: flag(object, "predicates")?,
            sorters: flag(object, "sorters")?,
            name_rules: object
                .get("name_rules")
                .map(|v| {
                    serde_json::from_value(v.clone())
                        .map_err(|_| "native_cpp.name_rules must be a string map".to_string())
                })
                .transpose()?
                .unwrap_or_default(),
            werror_doc_links: flag(object, "werror_doc_links")?,
        };
        rules::validate(&config.name_rules)?;
        Ok(config)
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
pub(crate) struct NativeCppResolver {
    config: NativeCppConfig,
    parents: BTreeMap<ModelPath, Vec<String>>,
    documentation: RefCell<Option<BTreeMap<String, String>>>,
    diagnostics: RefCell<BTreeSet<super::native_comments::DocWarning>>,
}
impl NativeCppResolver {
    pub(crate) fn new(graph: &Graph, config: NativeCppConfig) -> Result<Self, String> {
        validate_cpp_name_rules(&config.name_rules)?;
        let mut parents: BTreeMap<ModelPath, Vec<String>> = BTreeMap::new();
        let empty = BTreeMap::new();
        let ctx = Resolver {
            graph,
            config: &config,
            parents: &empty,
        };
        let indexed: Option<BTreeSet<String>> = graph.raw_comments.as_ref().and_then(|_| {
            let root = graph.root.as_ref().and_then(reference)?;
            let map = graph
                .nodes
                .get(root)?
                .properties
                .get("referenceMap")?
                .as_object()?;
            Some(
                map.values()
                    .filter_map(reference)
                    .map(str::to_owned)
                    .collect(),
            )
        });
        for (id, node) in &graph.nodes {
            if indexed.as_ref().is_some_and(|ids| !ids.contains(id)) {
                continue;
            }
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
        Ok(Self {
            config,
            parents,
            documentation: RefCell::new(None),
            diagnostics: RefCell::new(BTreeSet::new()),
        })
    }
    pub(crate) fn diagnostics(&self) -> Vec<String> {
        self.diagnostics
            .borrow()
            .iter()
            .map(|w| format!("{}: {}", w.scope, w.message))
            .collect()
    }
    pub(crate) fn documentation_names(
        &self,
        graph: &Graph,
    ) -> Result<BTreeMap<String, String>, String> {
        let ctx = Resolver {
            graph,
            config: &self.config,
            parents: &self.parents,
        };
        let root = graph.root.as_ref().ok_or("native C++ missing root")?;
        let map = ctx
            .get(root, "referenceMap")?
            .as_object()
            .ok_or("invalid reference map")?;
        let mut result = BTreeMap::new();
        for value in map.values() {
            let class = ctx.class(value)?.rsplit('.').next().unwrap_or("");
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
                continue;
            }
            let path = ctx.path(value)?;
            let key = path
                .head
                .iter()
                .chain(&path.tail)
                .cloned()
                .collect::<Vec<_>>()
                .join(".");
            match class {
                "LimeException" => {
                    result.insert(
                        key,
                        ctx.name(ctx.get(value, "errorType")?, &mut BTreeSet::new())?,
                    );
                }
                "LimeParameter" => {
                    let name = ctx.short_name(value)?;
                    if path.disambiguator.is_empty() {
                        result.insert(key, name);
                    } else {
                        result.insert(format!("{key}:{}", path.disambiguator), name.clone());
                        if let Some((owner, parameter)) = key.rsplit_once('.') {
                            result.insert(
                                format!("{owner}:{}.{parameter}", path.disambiguator),
                                name,
                            );
                        }
                    }
                }
                "LimeProperty" => {
                    let parent = ctx.parent(value)?.ok_or("property missing parent")?;
                    let base = ctx.full_name(&parent, &mut BTreeSet::new())?;
                    let getter = format!(
                        "{base}::{}",
                        ctx.accessor(value, "getter")?
                            .ok_or("property missing getter")?
                    );
                    result.insert(key.clone(), getter.clone());
                    result.insert(format!("{key}.get"), getter);
                    if !ctx.get(value, "setter")?.is_null() {
                        result.insert(
                            format!("{key}.set"),
                            format!(
                                "{base}::{}",
                                ctx.accessor(value, "setter")?
                                    .ok_or("property missing setter")?
                            ),
                        );
                    }
                }
                "LimeFunction" => {
                    let name = ctx.reference_name(value)?;
                    result.insert(key.clone(), name.clone());
                    let params = ctx
                        .get(value, "parameters")?
                        .as_array()
                        .ok_or("invalid parameters")?;
                    let signature = params
                        .iter()
                        .map(|p| ctx.lime_ref_string(ctx.get(p, "typeRef")?))
                        .collect::<Result<Vec<_>, _>>()?
                        .join(",");
                    result.insert(format!("{key}({signature})"), name);
                }
                _ => {
                    result.insert(key, ctx.full_name(value, &mut BTreeSet::new())?);
                }
            }
        }
        Ok(result)
    }
    pub(crate) fn signature(&self, graph: &Graph, function: &Value) -> Result<Vec<String>, String> {
        Resolver {
            graph,
            config: &self.config,
            parents: &self.parents,
        }
        .signature(function)
    }
    pub(crate) fn signature_type(&self, graph: &Graph, tr: &Value) -> Result<String, String> {
        let ctx = Resolver {
            graph,
            config: &self.config,
            parents: &self.parents,
        };
        if let Some(t) = ctx.attr(tr, "CPP", "TYPE")? {
            return t
                .as_str()
                .map(str::to_owned)
                .ok_or_else(|| "invalid C++ Type attribute".into());
        }
        ctx.signature_type(tr, &mut BTreeSet::new())
    }
    pub(crate) fn resolve(
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
        if mode == "name"
            && selector != "FQN"
            && ctx.class(receiver)? == "com.here.gluecodium.model.lime.LimeComment"
        {
            if let Some(text) = super::native_comments::selected(graph, receiver)? {
                if self.documentation.borrow().is_none() {
                    let map = self.documentation_names(graph)?;
                    *self.documentation.borrow_mut() = Some(map);
                }
                let scope = ctx.path(receiver)?;
                let mut scope_name = scope
                    .head
                    .iter()
                    .chain(&scope.tail)
                    .cloned()
                    .collect::<Vec<_>>()
                    .join(".");
                if !scope.disambiguator.is_empty() {
                    scope_name.push(':');
                    scope_name.push_str(&scope.disambiguator);
                }
                let (formatted, warnings) = super::native_comments::format_with_diagnostics(
                    &text,
                    &scope_name,
                    self.documentation.borrow().as_ref().unwrap(),
                    self.config.werror_doc_links,
                )?;
                self.diagnostics.borrow_mut().extend(warnings);
                return Ok(Some(formatted));
            }
        }
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
                    | "com.here.gluecodium.model.lime.LimeLazyTypeRef"
                    | "com.here.gluecodium.model.lime.LimePositionalTypeRef"
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
    fn lime_type_name(&self, ty: &Value) -> Result<String, String> {
        let class = self.class(ty)?.rsplit('.').next().unwrap_or("");
        if matches!(class, "LimeList" | "LimeSet" | "LimeMap") {
            let id = reference(ty).ok_or("invalid generic type")?;
            return self.generic_lime_name(ty, &mut BTreeSet::from([id.to_owned()]));
        }
        if class == "LimeBasicType" {
            return Ok(match self
                .get(ty, "typeId")?
                .get("name")
                .and_then(Value::as_str)
                .ok_or("invalid basic type")?
            {
                "VOID" => "Void",
                "INT8" => "Byte",
                "UINT8" => "UByte",
                "INT16" => "Short",
                "UINT16" => "UShort",
                "INT32" => "Int",
                "UINT32" => "UInt",
                "INT64" => "Long",
                "UINT64" => "ULong",
                "FLOAT" => "Float",
                "DOUBLE" => "Double",
                "BOOLEAN" => "Boolean",
                "STRING" => "String",
                "BLOB" => "Blob",
                "DATE" => "Date",
                "DURATION" => "Duration",
                "LOCALE" => "Locale",
                _ => return Err("invalid basic type".into()),
            }
            .into());
        }
        Ok(self.path(ty)?.tail.last().cloned().unwrap_or_default())
    }
    fn generic_lime_name(
        &self,
        ty: &Value,
        active: &mut BTreeSet<String>,
    ) -> Result<String, String> {
        let part = |tr: &Value, active: &mut BTreeSet<String>| -> Result<String, String> {
            let child = self.get(tr, "type")?;
            let class = self.class(child)?.rsplit('.').next().unwrap_or("");
            let name = if matches!(class, "LimeList" | "LimeSet" | "LimeMap") {
                let id = reference(child).ok_or("invalid generic type")?.to_owned();
                if !active.insert(id.clone()) || active.len() > 128 {
                    return Err("cyclic generic type".into());
                }
                let n = self.generic_lime_name(child, active)?;
                active.remove(&id);
                n
            } else {
                self.lime_type_name(child)?
            };
            let nullable = self
                .get(tr, "isNullable")?
                .as_bool()
                .ok_or("invalid nullable")?;
            Ok(format!("{name}{}", if nullable { "?" } else { "" }))
        };
        match self.class(ty)?.rsplit('.').next().unwrap_or("") {
            "LimeList" => Ok(format!(
                "List<{}>",
                part(self.get(ty, "elementType")?, active)?
            )),
            "LimeSet" => Ok(format!(
                "Set<{}>",
                part(self.get(ty, "elementType")?, active)?
            )),
            "LimeMap" => Ok(format!(
                "Map<{}, {}>",
                part(self.get(ty, "keyType")?, active)?,
                part(self.get(ty, "valueType")?, active)?
            )),
            _ => Err("invalid generic type".into()),
        }
    }
    fn lime_ref_string(&self, tr: &Value) -> Result<String, String> {
        Ok(format!(
            "{}{}",
            self.lime_type_name(self.get(tr, "type")?)?,
            if self
                .get(tr, "isNullable")?
                .as_bool()
                .ok_or("invalid nullable")?
            {
                "?"
            } else {
                ""
            }
        ))
    }
    fn signature_type(&self, tr: &Value, active: &mut BTreeSet<String>) -> Result<String, String> {
        let ty = self.get(tr, "type")?;
        let id = reference(ty).ok_or("invalid signature type")?.to_owned();
        if !active.insert(id.clone()) || active.len() > 128 {
            return Err("cyclic signature type".into());
        }
        let class = self.class(ty)?.rsplit('.').next().unwrap_or("");
        let name = match class {
            "LimeTypeAlias" => self.signature_type(self.get(ty, "typeRef")?, active)?,
            "LimeList" => format!(
                "[{}]",
                self.signature_type(self.get(ty, "elementType")?, active)?
            ),
            "LimeSet" => format!(
                "[{}:]",
                self.signature_type(self.get(ty, "elementType")?, active)?
            ),
            "LimeMap" => format!(
                "[{}:{}]",
                self.signature_type(self.get(ty, "keyType")?, active)?,
                self.signature_type(self.get(ty, "valueType")?, active)?
            ),
            _ => self.lime_type_name(ty)?,
        };
        active.remove(&id);
        let actual = self.actual(ty, &mut BTreeSet::new())?;
        let suffix = if self
            .get(tr, "isNullable")?
            .as_bool()
            .ok_or("invalid nullable")?
            && !self.is_pointer(&actual)?
        {
            "?"
        } else {
            ""
        };
        Ok(format!("{name}{suffix}"))
    }
    fn signature(&self, function: &Value) -> Result<Vec<String>, String> {
        self.get(function, "parameters")?
            .as_array()
            .ok_or("invalid parameters")?
            .iter()
            .map(|p| {
                let tr = self.get(p, "typeRef")?;
                if let Some(t) = self.attr(tr, "CPP", "TYPE")? {
                    return t
                        .as_str()
                        .map(str::to_owned)
                        .ok_or_else(|| "invalid C++ Type attribute".into());
                }
                self.signature_type(tr, &mut BTreeSet::new())
            })
            .collect()
    }
    fn signature_name(&self, function: &Value) -> Result<String, String> {
        if let Some(value) = self.attr(function, "CPP", "NAME")? {
            return value
                .as_str()
                .map(str::to_owned)
                .ok_or_else(|| "invalid C++ Name attribute".into());
        }
        let path = self.path(function)?;
        let name = path.tail.last().ok_or("missing function name")?;
        rules::name(&self.config.name_rules, "method", name, false)
    }
    fn reference_name(&self, function: &Value) -> Result<String, String> {
        let mut name = self.full_name(function, &mut BTreeSet::new())?;
        if let Some(parent) = self.parent(function)? {
            let target = self.signature_name(function)?;
            let functions = self
                .get(&parent, "functions")?
                .as_array()
                .ok_or("invalid functions")?;
            let mut count = 0;
            for f in functions {
                if self.signature_name(f)? == target {
                    count += 1;
                }
            }
            if count > 1 {
                let params = self
                    .get(function, "parameters")?
                    .as_array()
                    .ok_or("invalid parameters")?;
                let mut rendered = Vec::new();
                for p in params {
                    let tr = self.get(p, "typeRef")?;
                    let suffix =
                        if super::native_controls::predicate(self.graph, "needsRefSuffix", tr)? {
                            "&"
                        } else {
                            ""
                        };
                    rendered.push(format!(
                        "const {}{suffix}",
                        self.type_ref(tr, &mut BTreeSet::new())?
                    ));
                }
                name.push('(');
                name.push_str(&rendered.join(", "));
                name.push(')');
            }
        }
        Ok(name)
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
        if node.properties.contains_key("external") {
            self.external(v)?;
        }
        if node.properties.contains_key("attributes") {
            self.attributes(v)?;
        }
        Ok(())
    }
    fn external(&self, v: &Value) -> Result<Option<&'a serde_json::Map<String, Value>>, String> {
        let external = self.get(v, "external")?;
        if external.is_null() {
            return Ok(None);
        }
        let descriptors = self
            .get(external, "descriptors")?
            .as_object()
            .ok_or("invalid external descriptors")?;
        let Some((_, cpp)) = descriptors
            .iter()
            .find(|(k, _)| k.eq_ignore_ascii_case("cpp"))
        else {
            return Ok(None);
        };
        Ok(Some(cpp.as_object().ok_or("invalid C++ descriptor")?))
    }
    fn external_name(&self, v: &Value, key: &str) -> Result<Option<&'a str>, String> {
        self.external(v)?
            .and_then(|m| {
                m.iter()
                    .find(|(k, _)| k.eq_ignore_ascii_case(key))
                    .map(|(_, v)| v)
            })
            .map(|v| {
                v.as_str()
                    .ok_or_else(|| "invalid C++ external name".to_string())
            })
            .transpose()
    }
    fn is_external(&self, v: &Value, depth: usize) -> Result<bool, String> {
        if depth > 128 {
            return Err("native C++ parent depth limit exceeded".into());
        }
        if self.external(v)?.is_some() {
            return Ok(true);
        }
        match self.parent(v)? {
            Some(p) => self.is_external(&p, depth + 1),
            None => Ok(false),
        }
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
            None if self.graph.raw_comments.is_some() => Ok(None),
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
                | "LimeBasicType"
                | "LimeList"
                | "LimeSet"
                | "LimeMap"
        ) {
            return Err(format!("unsupported native C++ named element {class}"));
        }
        self.get(v, "external")?;
        if let Some(n) = self.external_name(v, "name")? {
            return Ok(n.to_owned());
        }
        if let Some(n) = self.attr(v, "CPP", "NAME")? {
            return n
                .as_str()
                .map(str::to_owned)
                .ok_or_else(|| "invalid C++ Name attribute".into());
        }
        let path = self.path(v)?;
        let type_name;
        let n = if matches!(class, "LimeBasicType" | "LimeList" | "LimeSet" | "LimeMap") {
            type_name = self.lime_type_name(v)?;
            &type_name
        } else {
            path.tail
                .last()
                .ok_or("native C++ named element has empty path")?
        };
        if self.is_external(v, 0)? {
            return Ok(n.to_owned());
        }
        let rule = match class {
            "LimeField" => "field",
            "LimeParameter" => "parameter",
            "LimeFunction" | "LimeFieldConstructor" => "method",
            "LimeConstant" => "constant",
            "LimeEnumerator" => "enumerator",
            "LimeEnumeration" | "LimeTypeAlias" | "LimeStruct" | "LimeClass" | "LimeInterface"
            | "LimeLambda" | "LimeBasicType" | "LimeList" | "LimeSet" | "LimeMap" => "type",
            "LimeProperty" => "property",
            "LimeException" => "error",
            _ => return Err(format!("unsupported native C++ named element {class}")),
        };
        let boolean = if class == "LimeProperty" {
            self.is_boolean(v)?
        } else {
            false
        };
        rules::name(&self.config.name_rules, rule, n, boolean)
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
        if self.external_name(v, "name")?.is_some() {
            active.remove(&id);
            return Ok(short);
        }
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
                if let Some(text) = super::native_comments::selected(self.graph, v)? {
                    super::native_comments::format(&text)
                } else if self.node(v)?.properties.get("isEmpty") == Some(&Value::Bool(true)) {
                    Ok(String::new())
                } else {
                    Err("native C++ nonempty or unavailable comment unsupported".into())
                }
            }
            "LimeReturnType" => self.type_ref(self.get(v, "typeRef")?, active),
            "LimeBasicTypeRef"
            | "LimeDirectTypeRef"
            | "LimeAmbiguousTypeRef"
            | "LimeLazyTypeRef"
            | "LimePositionalTypeRef" => self.type_ref(v, active),
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
                    return Ok(value.to_owned());
                }
                self.basic(self.get(&actual, "typeId")?, None)?;
                let id = self
                    .get(&actual, "typeId")?
                    .get("name")
                    .and_then(Value::as_str)
                    .ok_or("invalid literal type")?;
                match id {
                    "DATE" => Ok(format!(
                        "::std::chrono::system_clock::from_time_t({})",
                        epoch_seconds(value)
                            .map(|n| n.to_string())
                            .unwrap_or_else(|| "null".into())
                    )),
                    "LOCALE" => Ok(format!(
                        "{}(std::string{{\"{}\"}})",
                        self.internal("Locale"),
                        normalize_locale(value).unwrap_or_else(|| "null".into())
                    )),
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
            "LimeValue$Null" => Ok(format!(
                "{}()",
                self.type_ref(self.get(v, "typeRef")?, active)?
            )),
            "LimeValue$Special" => {
                let ty = self.get(self.get(v, "typeRef")?, "type")?;
                let float = self.class(ty)?.ends_with(".LimeBasicType")
                    && self.get(ty, "typeId")?.get("name").and_then(Value::as_str) == Some("FLOAT");
                let value = self
                    .get(v, "value")?
                    .get("name")
                    .and_then(Value::as_str)
                    .ok_or("invalid special value")?;
                let (sign, method) = match value {
                    "NAN" => ("", "quiet_NaN"),
                    "INFINITY" => ("", "infinity"),
                    "NEGATIVE_INFINITY" => ("-", "infinity"),
                    _ => return Err("invalid special value".into()),
                };
                Ok(format!(
                    "{sign}std::numeric_limits<{}>::{method}()",
                    if float { "float" } else { "double" }
                ))
            }
            "LimeValue$InitializerList" | "LimeValue$StructInitializer" => {
                let id = reference(v).ok_or("invalid value")?.to_owned();
                if !active.insert(id.clone()) || active.len() > 128 {
                    return Err("native C++ cyclic value dependency".into());
                }
                let values = self
                    .get(v, "values")?
                    .as_array()
                    .ok_or("invalid initializer values")?
                    .iter()
                    .map(|x| self.name(x, active))
                    .collect::<Result<Vec<_>, _>>()?
                    .join(", ");
                active.remove(&id);
                let tr = self.get(v, "typeRef")?;
                if class == "LimeValue$StructInitializer" {
                    Ok(format!(
                        "{}{{{values}}}",
                        self.type_name(self.get(tr, "type")?, true, Some(tr), active)?
                    ))
                } else {
                    let ty = self.actual(self.get(tr, "type")?, &mut BTreeSet::new())?;
                    if self.class(&ty)?.ends_with(".LimeBasicType")
                        && self.get(&ty, "typeId")?.get("name").and_then(Value::as_str)
                            == Some("BLOB")
                    {
                        Ok(format!("::std::make_shared<::std::vector<uint8_t>>(::std::vector<uint8_t>({{{values}}}))"))
                    } else {
                        Ok(format!("{{{values}}}"))
                    }
                }
            }
            "LimeValue$KeyValuePair" => {
                let id = reference(v).ok_or("invalid value")?.to_owned();
                if !active.insert(id.clone()) || active.len() > 128 {
                    return Err("native C++ cyclic value dependency".into());
                }
                let key = self.name(self.get(v, "key")?, active)?;
                let value = self.name(self.get(v, "value")?, active)?;
                active.remove(&id);
                Ok(format!("{{{key}, {value}}}"))
            }
            "LimeValue$Duration" => {
                let tr = self.get(v, "typeRef")?;
                let ty = self.basic(&serde_json::json!({"enum":"com.here.gluecodium.model.lime.LimeBasicType$TypeId","name":"DURATION"}), Some(tr))?;
                let unit = self
                    .get(v, "timeUnit")?
                    .get("name")
                    .and_then(Value::as_str)
                    .ok_or("invalid duration unit")?;
                let (factory, suffix) = match unit {
                    "DAY" => ("hours", " * 24"),
                    "HOUR" => ("hours", ""),
                    "MINUTE" => ("minutes", ""),
                    "SECOND" => ("seconds", ""),
                    "MILLISECOND" => ("milliseconds", ""),
                    "MICROSECOND" => ("microseconds", ""),
                    "NANOSECOND" => ("nanoseconds", ""),
                    _ => return Err("invalid duration unit".into()),
                };
                let value = self
                    .get(v, "value")?
                    .as_str()
                    .ok_or("invalid duration value")?;
                Ok(format!(
                    "::std::chrono::duration_cast<{ty}>(::std::chrono::{factory}({value}{suffix}))"
                ))
            }
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
        if let Some(name) = self.external_name(
            v,
            if mode == "getter" {
                "getterName"
            } else {
                "setterName"
            },
        )? {
            return Ok(Some(name.to_owned()));
        }
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
                if let Some(name) = self.external_name(accessor, "name")? {
                    return Ok(Some(name.to_owned()));
                }
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
        let boolean = mode == "getter" && self.is_boolean(v)?;
        Ok(Some(rules::name(
            &self.config.name_rules,
            mode,
            name,
            boolean,
        )?))
    }
    fn is_boolean(&self, v: &Value) -> Result<bool, String> {
        let actual = self.actual(
            self.get(self.get(v, "typeRef")?, "type")?,
            &mut BTreeSet::new(),
        )?;
        Ok(
            self.class(&actual)? == "com.here.gluecodium.model.lime.LimeBasicType"
                && self
                    .get(&actual, "typeId")?
                    .get("name")
                    .and_then(Value::as_str)
                    == Some("BOOLEAN"),
        )
    }
}
// Gregorian civil date conversion, matching Instant epoch seconds for ISO dates with an offset.
pub(crate) fn epoch_seconds(s: &str) -> Option<i64> {
    let split = s.find(['T', 't'])?;
    let (date, rest) = s.split_at(split);
    let time = &rest[1..];
    let sign = if date.starts_with('-') { -1 } else { 1 };
    let signed = date.starts_with(['-', '+']);
    let unsigned = if signed { &date[1..] } else { date };
    let mut d = unsigned.split('-');
    let year = d.next()?;
    let month = d.next()?;
    let day = d.next()?;
    if d.next().is_some()
        || !(4..=9).contains(&year.len())
        || !year.bytes().all(|c| c.is_ascii_digit())
        || (!signed && year.len() != 4)
        || (date.starts_with('+') && year.len() <= 4)
        || (date.starts_with('-') && year.bytes().all(|c| c == b'0'))
    {
        return None;
    }
    let two = |v: &str| -> Option<i64> {
        if v.len() != 2 || !v.bytes().all(|c| c.is_ascii_digit()) {
            None
        } else {
            v.parse().ok()
        }
    };
    let y = sign * year.parse::<i64>().ok()?;
    let m = two(month)?;
    let day = two(day)?;
    if !(1..=12).contains(&m) {
        return None;
    }
    let leap = y % 4 == 0 && (y % 100 != 0 || y % 400 == 0);
    let max_day = match m {
        2 if leap => 29,
        2 => 28,
        4 | 6 | 9 | 11 => 30,
        _ => 31,
    };
    if !(1..=max_day).contains(&day) {
        return None;
    }
    let time = if let Some((head, zone)) = time.split_once('[') {
        if !zone.ends_with(']') || zone.len() < 2 || zone[..zone.len() - 1].contains(['[', ']']) {
            return None;
        }
        head
    } else {
        time
    };
    let (clock, offset) = if let Some(c) = time.strip_suffix(['Z', 'z']) {
        (c, 0)
    } else {
        let pos = time
            .char_indices()
            .skip(1)
            .find(|(_, c)| *c == '+' || *c == '-')?
            .0;
        let sign = if &time[pos..pos + 1] == "+" { 1 } else { -1 };
        let mut o = time[pos + 1..].split(':');
        let h = two(o.next()?)?;
        let m = two(o.next()?)?;
        let sec = match o.next() {
            Some(value) => two(value)?,
            None => 0,
        };
        if o.next().is_some() || h > 18 || m > 59 || sec > 59 || (h == 18 && (m != 0 || sec != 0)) {
            return None;
        }
        (&time[..pos], sign * (h * 3600 + m * 60 + sec))
    };
    let mut t = clock.split(':');
    let h = two(t.next()?)?;
    let min = two(t.next()?)?;
    let sec = if let Some(s) = t.next() {
        let (sec, fraction) = s.split_once('.').map_or((s, None), |(a, b)| (a, Some(b)));
        if fraction.is_some_and(|f| f.len() > 9 || !f.bytes().all(|c| c.is_ascii_digit())) {
            return None;
        }
        two(sec)?
    } else {
        0
    };
    if t.next().is_some() || h > 23 || min > 59 || sec > 59 {
        return None;
    }
    let y = y - i64::from(m <= 2);
    let era = y.div_euclid(400);
    let yoe = y - era * 400;
    let mp = m + if m > 2 { -3 } else { 9 };
    let days =
        era * 146097 + yoe * 365 + yoe / 4 - yoe / 100 + (153 * mp + 2) / 5 + day - 1 - 719468;
    Some(days * 86400 + h * 3600 + min * 60 + sec - offset)
}
pub(crate) fn normalize_locale(s: &str) -> Option<String> {
    let tag = s.trim();
    if tag.eq_ignore_ascii_case("und") {
        return Some("und".into());
    }
    let lower = tag.to_ascii_lowercase();
    let replacement = match lower.as_str() {
        "art-lojban" => Some("jbo"),
        "en-gb-oed" => Some("en-GB-x-oed"),
        "i-default" => Some("en-x-i-default"),
        "i-enochian" => Some("x-i-enochian"),
        "i-mingo" => Some("see-x-i-mingo"),
        "zh-min" => Some("nan-x-zh-min"),
        "cel-gaulish" => Some("xtg-x-cel-gaulish"),
        "i-ami" => Some("ami"),
        "i-bnn" => Some("bnn"),
        "i-hak" => Some("hak"),
        "i-klingon" => Some("tlh"),
        "i-lux" => Some("lb"),
        "i-navajo" => Some("nv"),
        "i-pwn" => Some("pwn"),
        "i-tao" => Some("tao"),
        "i-tay" => Some("tay"),
        "i-tsu" => Some("tsu"),
        "no-bok" => Some("nb"),
        "no-nyn" => Some("nn"),
        "sgn-be-fr" => Some("sfb"),
        "sgn-be-nl" => Some("vgt"),
        "sgn-ch-de" => Some("sgg"),
        "zh-guoyu" => Some("cmn"),
        "zh-hakka" => Some("hak"),
        "zh-min-nan" => Some("nan"),
        "zh-xiang" => Some("hsn"),
        _ => None,
    };
    if let Some(v) = replacement {
        return Some(v.into());
    }
    let parts: Vec<&str> = tag.split('-').collect();
    let alpha = |p: &str| p.chars().all(|c| c.is_ascii_alphabetic());
    let alnum = |p: &str| p.chars().all(|c| c.is_ascii_alphanumeric());
    if parts.first()?.eq_ignore_ascii_case("x") {
        let private: Vec<_> = parts
            .iter()
            .skip(1)
            .take_while(|p| (1..=8).contains(&p.len()) && alnum(p))
            .map(|p| p.to_ascii_lowercase())
            .collect();
        return (!private.is_empty()).then(|| format!("x-{}", private.join("-")));
    }
    let first = parts[0];
    if !(2..=8).contains(&first.len()) || !alpha(first) {
        return None;
    }
    let mut language = first.to_ascii_lowercase();
    let mut index = 1;
    if first.len() <= 3 {
        let mut extlangs = 0;
        while index < parts.len() && extlangs < 3 && parts[index].len() == 3 && alpha(parts[index])
        {
            if extlangs == 0 {
                language = parts[index].to_ascii_lowercase();
            }
            index += 1;
            extlangs += 1;
        }
    }
    language = match language.as_str() {
        "iw" => "he".into(),
        "ji" => "yi".into(),
        "in" => "id".into(),
        _ => language,
    };
    let mut output = Vec::new();
    let has_language = language != "und";
    if has_language {
        output.push(language);
    }
    if index < parts.len() && parts[index].len() == 4 && alpha(parts[index]) {
        let mut c = parts[index].chars();
        let mut script = c.next()?.to_ascii_uppercase().to_string();
        script.push_str(&c.as_str().to_ascii_lowercase());
        output.push(script);
        index += 1;
    }
    if index < parts.len()
        && ((parts[index].len() == 2 && alpha(parts[index]))
            || (parts[index].len() == 3 && parts[index].chars().all(|c| c.is_ascii_digit())))
    {
        output.push(parts[index].to_ascii_uppercase());
        index += 1;
    }
    while index < parts.len() {
        let p = parts[index];
        if ((5..=8).contains(&p.len()) || (p.len() == 4 && p.as_bytes()[0].is_ascii_digit()))
            && alnum(p)
        {
            output.push(p.to_owned());
            index += 1;
        } else {
            break;
        }
    }
    let mut extensions = BTreeMap::<String, Vec<String>>::new();
    while index < parts.len() && parts[index].len() == 1 && alnum(parts[index]) {
        let key = parts[index].to_ascii_lowercase();
        index += 1;
        let start = index;
        while index < parts.len()
            && (if key == "x" { 1..=8 } else { 2..=8 }).contains(&parts[index].len())
            && alnum(parts[index])
        {
            index += 1;
        }
        if index == start {
            break;
        }
        extensions.entry(key.clone()).or_insert_with(|| {
            parts[start..index]
                .iter()
                .map(|p| p.to_ascii_lowercase())
                .collect()
        });
        if key == "x" {
            break;
        }
    }
    for (key, values) in extensions {
        output.push(key.clone());
        if key == "u" {
            let mut attrs = BTreeSet::new();
            let mut keywords = BTreeMap::<String, Vec<String>>::new();
            let mut i = 0;
            while i < values.len() && values[i].len() >= 3 {
                attrs.insert(values[i].clone());
                i += 1;
            }
            while i < values.len() {
                let keyword = values[i].clone();
                i += 1;
                let start = i;
                while i < values.len() && values[i].len() >= 3 {
                    i += 1;
                }
                keywords
                    .entry(keyword)
                    .or_insert_with(|| values[start..i].to_vec());
            }
            output.extend(attrs);
            for (keyword, value) in keywords {
                output.push(keyword);
                output.extend(value);
            }
        } else {
            output.extend(values);
        }
    }
    if output.is_empty() {
        None
    } else {
        if !has_language && output[0] != "x" {
            output.insert(0, "und".into());
        }
        Some(output.join("-"))
    }
}
#[cfg(test)]
mod value_tests {
    use super::{epoch_seconds, normalize_locale};
    #[test]
    fn date_offsets_and_locale_tags() {
        assert_eq!(epoch_seconds("1970-01-01T00:00:00Z"), Some(0));
        assert_eq!(epoch_seconds("1969-12-31T18:30:00-05:30"), Some(0));
        assert_eq!(epoch_seconds("2000-02-29T00:00:00Z"), Some(951782400));
        assert_eq!(epoch_seconds("not a date"), None);
        assert_eq!(epoch_seconds("2020-1-1T0:00Z"), None);
        assert_eq!(epoch_seconds("2020-01-01t00:00z"), Some(1577836800));
        assert_eq!(epoch_seconds("2020-01-01T00:00:00+18:01"), None);
        assert_eq!(
            epoch_seconds("2020-01-01T00:00:00+01:02:03"),
            Some(1577833077)
        );
        assert_eq!(epoch_seconds("2020-01-01T00:00:00.1234567890Z"), None);
        assert_eq!(epoch_seconds("-0001-01-01T00:00Z"), Some(-62198755200));
        assert_eq!(normalize_locale("EN-latn-us"), Some("en-Latn-US".into()));
        assert_eq!(normalize_locale("und"), Some("und".into()));
        assert_eq!(normalize_locale("und-US"), Some("und-US".into()));
        assert_eq!(normalize_locale("iw-IL"), Some("he-IL".into()));
        assert_eq!(normalize_locale("en-GB-oed"), Some("en-GB-x-oed".into()));
        assert_eq!(normalize_locale("i-default"), Some("en-x-i-default".into()));
        assert_eq!(normalize_locale("x-private"), Some("x-private".into()));
        assert_eq!(normalize_locale("en-abc"), Some("abc".into()));
        assert_eq!(normalize_locale("und-foo"), Some("foo".into()));
        assert_eq!(
            normalize_locale("en-u-nu-latn-ca-gregory"),
            Some("en-u-ca-gregory-nu-latn".into())
        );
        assert_eq!(
            normalize_locale("und-u-ca-gregory"),
            Some("und-u-ca-gregory".into())
        );
        assert_eq!(
            normalize_locale("en-419-FOOBAR"),
            Some("en-419-FOOBAR".into())
        );
        assert_eq!(
            normalize_locale("gsw-u-sd-chzh"),
            Some("gsw-u-sd-chzh".into())
        );
    }
}

#[cfg(test)]
mod documentation_tests {
    use super::{NativeCppConfig, NativeCppResolver};
    use crate::template::Graph;
    use serde_json::{json, Value};

    #[test]
    fn overloaded_parameter_scope_and_rendered_warnings() {
        let n = |id: &str, kind: &str, properties: Value| json!({"id":id,"class":format!("com.here.gluecodium.model.lime.{kind}"),"properties":properties});
        let nodes = vec![
            n(
                "root",
                "LimeModel",
                json!({"referenceMap": {"smoke.Owner":{"$ref":"owner"}, "smoke.Owner.f:1":{"$ref":"fun"}, "smoke.Owner.f.stuff:1":{"$ref":"param"}}}),
            ),
            n("attrs", "LimeAttributes", json!({"attributes":{}})),
            n(
                "ownerPath",
                "LimePath",
                json!({"head":["smoke"],"tail":["Owner"],"disambiguator":""}),
            ),
            n(
                "funPath",
                "LimePath",
                json!({"head":["smoke"],"tail":["Owner","f"],"disambiguator":"1"}),
            ),
            n(
                "paramPath",
                "LimePath",
                json!({"head":["smoke"],"tail":["Owner","f","stuff"],"disambiguator":"1"}),
            ),
            n(
                "owner",
                "LimeClass",
                json!({"path":{"$ref":"ownerPath"},"attributes":{"$ref":"attrs"},"external":null,"functions":[{"$ref":"fun"}]}),
            ),
            n(
                "fun",
                "LimeFunction",
                json!({"path":{"$ref":"funPath"},"attributes":{"$ref":"attrs"},"external":null,"parameters":[{"$ref":"param"}]}),
            ),
            n(
                "param",
                "LimeParameter",
                json!({"path":{"$ref":"paramPath"},"attributes":{"$ref":"attrs"},"external":null,"typeRef":{"$ref":"ref"}}),
            ),
            n(
                "ref",
                "LimeBasicTypeRef",
                json!({"type":{"$ref":"type"},"attributes":{"$ref":"attrs"},"isNullable":false}),
            ),
            n(
                "type",
                "LimeBasicType",
                json!({"typeId":{"enum":"com.here.gluecodium.model.lime.LimeBasicType$TypeId","name":"STRING"}}),
            ),
            n(
                "comment",
                "LimeComment",
                json!({"path":{"$ref":"funPath"},"placeholders":{}}),
            ),
        ];
        let snapshot = json!({"schema":"gluecodium.reference-model.snapshot","version":1,"root":{"$ref":"root"},"nodes":nodes});
        let mut graph = Graph::import(Some(&snapshot), None).unwrap();
        graph
            .attach_raw_comments(&json!({"comment":[["", "[stuff] [missing]"]]}))
            .unwrap();
        let resolver = NativeCppResolver::new(&graph, NativeCppConfig::default()).unwrap();
        let comment = json!({"$ref":"comment"});
        assert_eq!(
            resolver.resolve(&graph, "", "name", &comment).unwrap(),
            Some("stuff [missing]".into())
        );
        resolver.resolve(&graph, "", "name", &comment).unwrap();
        assert_eq!(
            resolver.diagnostics(),
            vec!["smoke.Owner.f:1: Failed to resolve documentation reference [missing]"]
        );
    }
    #[test]
    fn overload_names_ignore_external_descriptor_names() {
        use super::Resolver;
        use std::collections::BTreeMap;
        let node = |id: &str, kind: &str, properties: Value| json!({"id":id,"class":format!("com.here.gluecodium.model.lime.{kind}"),"properties":properties});
        let snapshot = json!({"schema":"gluecodium.reference-model.snapshot","version":1,"root":{"$ref":"root"},"nodes":[
            node("root", "LimeModel", json!({})),
            node("path", "LimePath", json!({"head":["smoke"],"tail":["Owner","doWork"],"disambiguator":""})),
            node("attrs", "LimeAttributes", json!({"attributes":{"CPP":{"NAME":"mapped"}}})),
            node("external", "LimeExternalDescriptor", json!({"descriptors":{"cpp":{"name":"External::renamed"}}})),
            node("function", "LimeFunction", json!({"path":{"$ref":"path"},"attributes":{"$ref":"attrs"},"external":{"$ref":"external"}}))
        ]});
        let mut graph = Graph::import(Some(&snapshot), None).unwrap();
        let config = NativeCppConfig::default();
        let parents = BTreeMap::new();
        let function = json!({"$ref":"function"});
        let resolver = Resolver {
            graph: &graph,
            config: &config,
            parents: &parents,
        };
        assert_eq!(resolver.short_name(&function).unwrap(), "External::renamed");
        assert_eq!(resolver.signature_name(&function).unwrap(), "mapped");
        graph.nodes.get_mut("attrs").unwrap().properties["attributes"] = json!({});
        let resolver = Resolver {
            graph: &graph,
            config: &config,
            parents: &parents,
        };
        assert_eq!(resolver.signature_name(&function).unwrap(), "do_work");
    }
}
