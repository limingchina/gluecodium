use serde_json::{Map, Value};
use std::collections::{BTreeMap, BTreeSet};

const ATTRIBUTE_VIEW: &str = "$ruscodium.attribute-view";

#[derive(Clone, Debug)]
pub struct ModelNode {
    pub class: String,
    pub properties: Map<String, Value>,
}
#[derive(Clone, Debug, Default)]
pub struct Graph {
    pub nodes: BTreeMap<String, ModelNode>,
    pub root: Option<Value>,
    absent: BTreeMap<String, BTreeSet<String>>,
    pub(super) raw_comments: Option<super::native_comments::RawComments>,
}
impl Graph {
    pub fn import(snapshot: Option<&Value>, overlays: Option<&Value>) -> Result<Self, String> {
        Self::import_with_absences(snapshot, overlays, None)
    }
    pub fn import_with_absences(
        snapshot: Option<&Value>,
        overlays: Option<&Value>,
        absences: Option<&Value>,
    ) -> Result<Self, String> {
        let mut graph = Self::default();
        if let Some(s) = snapshot {
            if s.get("schema").and_then(Value::as_str)
                != Some("gluecodium.reference-model.snapshot")
                || s.get("version").and_then(Value::as_u64) != Some(1)
            {
                return Err("unsupported reference snapshot schema or version".into());
            }
            let nodes = s
                .get("nodes")
                .and_then(Value::as_array)
                .ok_or("snapshot nodes must be an array")?;
            if nodes.len() > 1_000_000 {
                return Err("snapshot node limit exceeded".into());
            }
            for n in nodes {
                let id = n
                    .get("id")
                    .and_then(Value::as_str)
                    .filter(|s| !s.is_empty())
                    .ok_or("snapshot node has invalid id")?;
                let class = n
                    .get("class")
                    .and_then(Value::as_str)
                    .filter(|s| !s.is_empty())
                    .ok_or("snapshot node has invalid class")?;
                let properties = n
                    .get("properties")
                    .and_then(Value::as_object)
                    .ok_or("snapshot node has invalid properties")?;
                if graph
                    .nodes
                    .insert(
                        id.to_string(),
                        ModelNode {
                            class: class.to_string(),
                            properties: properties.clone(),
                        },
                    )
                    .is_some()
                {
                    return Err(format!("duplicate snapshot id {id}"));
                }
            }
            graph.root = Some(s.get("root").ok_or("snapshot has no root")?.clone());
        }
        if let Some(o) = overlays {
            for (id, fields) in o.as_object().ok_or("property_overlays must be an object")? {
                let node = graph
                    .nodes
                    .get_mut(id)
                    .ok_or_else(|| format!("overlay references unknown node {id}"))?;
                for (k, v) in fields.as_object().ok_or("overlay must be an object")? {
                    if node.properties.get(k).is_some_and(|existing| existing != v) {
                        return Err(format!(
                            "overlay conflicts with stored property {k} on {id}"
                        ));
                    }
                    node.properties.insert(k.clone(), v.clone());
                }
            }
        }
        if let Some(absences) = absences {
            let properties = graph.class_properties();
            for (id, names) in absences
                .as_object()
                .ok_or("absent_properties must be an object")?
            {
                let node = graph
                    .nodes
                    .get(id)
                    .ok_or_else(|| format!("absent_properties references unknown node {id}"))?;
                let mut set = BTreeSet::new();
                for name in names
                    .as_array()
                    .ok_or("absent property list must be an array")?
                {
                    let name = name
                        .as_str()
                        .filter(|s| !s.is_empty())
                        .ok_or("invalid absent property name")?;
                    if !set.insert(name.to_string()) {
                        return Err(format!("duplicate absent property {name} on {id}"));
                    }
                    if properties
                        .get(node.class.as_str())
                        .is_some_and(|names| names.contains(name))
                    {
                        return Err(format!(
                            "absent property {name} conflicts with stored property on class {}",
                            node.class
                        ));
                    }
                }
                graph.absent.insert(id.clone(), set);
            }
        }
        if let Some(root) = &graph.root {
            validate_value(root, &graph.nodes, 0)?;
            if reference(root).is_none() {
                return Err("snapshot root must be a reference".into());
            }
        }
        for n in graph.nodes.values() {
            for v in n.properties.values() {
                validate_value(v, &graph.nodes, 0)?;
            }
        }
        Ok(graph)
    }
    pub(crate) fn class_properties(&self) -> BTreeMap<String, BTreeSet<String>> {
        let mut classes: BTreeMap<String, BTreeSet<String>> = BTreeMap::new();
        for node in self.nodes.values() {
            classes
                .entry(node.class.clone())
                .or_default()
                .extend(node.properties.keys().cloned());
        }
        classes
    }
    pub(crate) fn attach_raw_comments(&mut self, raw: &Value) -> Result<(), String> {
        self.raw_comments = Some(super::native_comments::import(self, raw)?);
        Ok(())
    }
    pub fn validate(&self, value: &Value) -> Result<(), String> {
        validate_value(value, &self.nodes, 0)
    }
    pub fn property(&self, value: &Value, key: &str) -> Result<Option<Value>, String> {
        if let Some(id) = reference(value) {
            let node = self
                .nodes
                .get(id)
                .ok_or_else(|| format!("dangling reference {id}"))?;
            if node.class == "com.here.gluecodium.model.lime.LimeComment" && key == "isEmpty" {
                if let Some(raw) = &self.raw_comments {
                    let sections = raw.get(id).ok_or("missing raw comment")?;
                    return Ok(Some(Value::Bool(
                        sections.iter().all(|(_, text)| text.is_empty()),
                    )));
                }
            }
            if node.class == "com.here.gluecodium.model.lime.LimeLambdaParameter"
                && key == "parameterName"
                && self.raw_comments.is_some()
            {
                let path = node
                    .properties
                    .get("path")
                    .ok_or("missing lambda parameter path")?;
                let path_id = reference(path).ok_or("invalid lambda parameter path")?;
                let tail = self
                    .nodes
                    .get(path_id)
                    .and_then(|n| n.properties.get("tail"))
                    .and_then(Value::as_array)
                    .ok_or("invalid lambda parameter path tail")?;
                return Ok(Some(
                    tail.last()
                        .and_then(Value::as_str)
                        .ok_or("empty lambda parameter path")?
                        .into(),
                ));
            }
            if node.class == "com.here.gluecodium.model.lime.LimeAttributes" {
                let attributes = node
                    .properties
                    .get("attributes")
                    .and_then(Value::as_object)
                    .ok_or("invalid LimeAttributes snapshot")?;
                if key == "size" {
                    return Ok(Some(Value::from(attributes.len())));
                }
                if key == "isEmpty" {
                    return Ok(Some(Value::Bool(attributes.is_empty())));
                }
                return Ok(attributes
                    .iter()
                    .find(|(k, _)| attribute_key(k) == key.to_lowercase())
                    .map(|(_, v)| match v {
                        Value::Object(fields) => {
                            let folded: Map<String, Value> = fields
                                .iter()
                                .map(|(k, v)| (attribute_key(k), v.clone()))
                                .collect();
                            Value::Object(Map::from_iter([(
                                ATTRIBUTE_VIEW.to_string(),
                                Value::Object(folded),
                            )]))
                        }
                        _ => v.clone(),
                    }));
            }
            if self.absent.get(id).is_some_and(|names| names.contains(key)) {
                return Ok(None);
            }
            return node
                .properties
                .get(key)
                .cloned()
                .map(Some)
                .ok_or_else(|| format!("unsupported property {key} on {} ({id})", node.class));
        }
        match value {
            Value::Object(m) if m.len() == 1 && m.contains_key(ATTRIBUTE_VIEW) => {
                let fields = m[ATTRIBUTE_VIEW]
                    .as_object()
                    .ok_or("invalid attribute view")?;
                let key = key.to_lowercase();
                if let Some(value) = fields.get(&key) {
                    return Ok(Some(value.clone()));
                }
                if key == "isempty" {
                    return Ok(Some(Value::Bool(fields.is_empty())));
                }
                Ok(None)
            }
            Value::Object(m) if m.contains_key("enum") && key == "toString" => {
                let class = m
                    .get("enum")
                    .and_then(Value::as_str)
                    .ok_or("invalid enum class")?;
                let name = m
                    .get("name")
                    .and_then(Value::as_str)
                    .ok_or("invalid enum name")?;
                if class == "com.here.gluecodium.model.lime.LimeBasicType$TypeId" {
                    let tag = match name {
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
                        _ => return Err(format!("unsupported enum value {class}.{name}")),
                    };
                    Ok(Some(Value::String(tag.into())))
                } else {
                    Err(format!("unsupported enum toString on {class}"))
                }
            }
            Value::Object(m) => Ok(m.get(key).cloned()),
            Value::Array(a) if key.parse::<usize>().is_ok() => {
                Ok(a.get(key.parse::<usize>().unwrap()).cloned())
            }
            Value::Array(a) if key == "size" => Ok(Some(Value::from(a.len()))),
            Value::Array(a) if key == "isEmpty" => Ok(Some(Value::Bool(a.is_empty()))),
            Value::String(s) if key == "length" => Ok(Some(Value::from(s.encode_utf16().count()))),
            Value::String(s) if key == "isEmpty" => Ok(Some(Value::Bool(s.is_empty()))),
            _ => Ok(None),
        }
    }
    pub fn class<'a>(&'a self, value: &'a Value) -> Option<&'a str> {
        reference(value)
            .and_then(|id| self.nodes.get(id).map(|n| n.class.as_str()))
            .or_else(|| value.get("enum").and_then(Value::as_str))
            .or(match value {
                Value::String(_) => Some("java.lang.String"),
                Value::Bool(_) => Some("java.lang.Boolean"),
                _ => None,
            })
    }
}
pub fn reference(v: &Value) -> Option<&str> {
    let m = v.as_object()?;
    if m.len() == 1 {
        m.get("$ref")?.as_str()
    } else {
        None
    }
}
fn validate_value(
    v: &Value,
    nodes: &BTreeMap<String, ModelNode>,
    depth: usize,
) -> Result<(), String> {
    if depth > 128 {
        return Err("graph value nesting limit exceeded".into());
    }
    match v {
        Value::Object(m) => {
            if m.contains_key(ATTRIBUTE_VIEW) {
                return Err("reserved attribute view key in input".into());
            }
            if m.contains_key("$ref") {
                let id = reference(v).ok_or("invalid reference object")?;
                if !nodes.contains_key(id) {
                    return Err(format!("dangling reference {id}"));
                }
            } else {
                for v in m.values() {
                    validate_value(v, nodes, depth + 1)?;
                }
            }
        }
        Value::Array(a) => {
            for v in a {
                validate_value(v, nodes, depth + 1)?;
            }
        }
        _ => {}
    }
    Ok(())
}

fn attribute_key(key: &str) -> String {
    key.chars()
        .filter(|c| *c != '_')
        .flat_map(char::to_lowercase)
        .collect()
}
