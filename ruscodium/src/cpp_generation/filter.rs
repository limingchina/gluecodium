//! Filter model declarations using Gluecodium's platform and tag predicates.
use super::{array, class, field, ref_id};
use crate::template::Graph;
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};

fn matches_tags(value: Option<&Value>, tags: &BTreeSet<&str>) -> Option<bool> {
    match value? {
        Value::Bool(true) => Some(true),
        Value::String(tag) => Some(tags.iter().any(|v| v.eq_ignore_ascii_case(tag))),
        Value::Array(items) => Some(
            items
                .iter()
                .filter_map(Value::as_str)
                .any(|tag| tags.iter().any(|v| v.eq_ignore_ascii_case(tag))),
        ),
        _ => None,
    }
}
fn retain(graph: &Graph, element: &Value, tags: &BTreeSet<&str>) -> Result<bool, String> {
    let attrs = field(graph, element, "attributes")?;
    let attrs = graph
        .nodes
        .get(ref_id(&attrs)?)
        .and_then(|n| n.properties.get("attributes"))
        .and_then(Value::as_object)
        .ok_or("invalid attributes")?;
    for (group, enable, skip) in [
        ("ENABLE_IF", "TAG", None),
        ("SKIP", "", Some("TAG")),
        ("CPP", "ENABLE_IF", Some("SKIP")),
    ] {
        let values = attrs.get(group).and_then(Value::as_object);
        if !enable.is_empty()
            && matches_tags(values.and_then(|v| v.get(enable)), tags) == Some(false)
        {
            return Ok(false);
        }
        if skip.is_some_and(|key| matches_tags(values.and_then(|v| v.get(key)), tags) == Some(true))
        {
            return Ok(false);
        }
    }
    Ok(true)
}
const MEMBERS: &[&str] = &[
    "structs",
    "enumerations",
    "constants",
    "typeAliases",
    "functions",
    "properties",
    "exceptions",
    "classes",
    "interfaces",
    "lambdas",
    "fields",
    "fieldConstructors",
    "enumerators",
];
fn walk(
    graph: &Graph,
    element: &Value,
    tags: &BTreeSet<&str>,
    retained: &mut BTreeSet<String>,
    updates: &mut BTreeMap<String, BTreeMap<String, Value>>,
) -> Result<(), String> {
    let id = ref_id(element)?.to_owned();
    retained.insert(id.clone());
    let kind = class(graph, element)?;
    if kind == "LimeProperty" {
        let setter = field(graph, element, "setter")?;
        if !setter.is_null() && !retain(graph, &setter, tags)? {
            updates
                .entry(id)
                .or_default()
                .insert("setter".into(), Value::Null);
        }
        return Ok(());
    }
    if !matches!(
        kind,
        "LimeClass" | "LimeInterface" | "LimeStruct" | "LimeEnumeration"
    ) {
        return Ok(());
    }
    for key in MEMBERS {
        if graph.nodes[&id].properties.contains_key(*key) {
            let mut members = Vec::new();
            for item in array(graph, element, key)? {
                if retain(graph, &item, tags)? {
                    walk(graph, &item, tags, retained, updates)?;
                    members.push(item);
                }
            }
            updates
                .entry(id.clone())
                .or_default()
                .insert((*key).into(), json!(members));
        }
    }
    Ok(())
}
pub(super) fn apply(graph: &mut Graph, active_tags: &[String]) -> Result<(), String> {
    let tags = active_tags
        .iter()
        .map(String::as_str)
        .collect::<BTreeSet<_>>();
    let root = graph.root.clone().ok_or("missing model root")?;
    let root_id = ref_id(&root)?.to_owned();
    let mut retained = BTreeSet::new();
    let mut updates = BTreeMap::<String, BTreeMap<String, Value>>::new();
    for key in ["topElements", "auxiliaryElements"] {
        let mut result = Vec::new();
        for element in array(graph, &root, key)? {
            if retain(graph, &element, &tags)? {
                walk(graph, &element, &tags, &mut retained, &mut updates)?;
                result.push(element);
            }
        }
        updates
            .entry(root_id.clone())
            .or_default()
            .insert(key.into(), json!(result));
    }
    let refs = field(graph, &root, "referenceMap")?;
    let refs = refs.as_object().ok_or("invalid reference map")?;
    let mut filtered = serde_json::Map::new();
    let dropped = refs
        .iter()
        .filter_map(|(key, value)| {
            let id = ref_id(value).ok()?;
            let kind = graph.nodes.get(id)?.class.rsplit('.').next()?;
            (matches!(
                kind,
                "LimeClass"
                    | "LimeInterface"
                    | "LimeStruct"
                    | "LimeEnumeration"
                    | "LimeException"
                    | "LimeTypeAlias"
                    | "LimeLambda"
                    | "LimeConstant"
                    | "LimeField"
                    | "LimeFieldConstructor"
                    | "LimeFunction"
                    | "LimeProperty"
                    | "LimeEnumerator"
            ) && !retained.contains(id))
            .then(|| key.clone())
        })
        .collect::<BTreeSet<_>>();
    for (key, value) in refs {
        let node = graph
            .nodes
            .get(ref_id(value)?)
            .ok_or("invalid reference map node")?;
        let mut retained_parameter_parent = None;
        if node.class.ends_with(".LimeParameter") {
            let path = field(graph, value, "path")?;
            let suffix = field(graph, &path, "disambiguator")?;
            let suffix = suffix.as_str().ok_or("invalid parameter disambiguator")?;
            if !suffix.is_empty() {
                let head = array(graph, &path, "head")?;
                let tail = array(graph, &path, "tail")?;
                let mut parent = head
                    .iter()
                    .chain(tail.iter().take(tail.len().saturating_sub(1)))
                    .map(|v| v.as_str().ok_or("invalid parameter path"))
                    .collect::<Result<Vec<_>, _>>()?
                    .join(".");
                let ambiguous = parent.clone();
                parent.push(':');
                parent.push_str(suffix);
                if dropped.contains(&parent) {
                    continue;
                }
                retained_parameter_parent = Some(ambiguous);
            }
        }
        let mut prefixes = key
            .match_indices('.')
            .map(|(i, _)| &key[..i])
            .collect::<Vec<_>>();
        prefixes.push(key);
        if prefixes.into_iter().any(|name| {
            dropped.contains(name) && retained_parameter_parent.as_deref() != Some(name)
        }) {
            continue;
        }
        filtered.insert(key.clone(), value.clone());
    }
    let numbered: Vec<_> = filtered
        .iter()
        .filter_map(|(key, value)| {
            key.split_once(':')
                .map(|(base, _)| (base.to_owned(), value.clone()))
        })
        .collect();
    for (base, value) in numbered {
        filtered.entry(base).or_insert(value);
    }
    updates
        .entry(root_id)
        .or_default()
        .insert("referenceMap".into(), Value::Object(filtered));
    for (id, fields) in updates {
        graph
            .nodes
            .get_mut(&id)
            .ok_or("missing filtered node")?
            .properties
            .extend(fields);
    }
    let structs = graph
        .nodes
        .iter()
        .filter(|(_, n)| n.class.ends_with(".LimeStruct"))
        .map(|(id, _)| id.clone())
        .collect::<Vec<_>>();
    for id in structs {
        let element = json!({"$ref":id});
        let children = array(graph, &element, "fields")?
            .iter()
            .map(|f| field(graph, f, "typeRef"))
            .collect::<Result<Vec<_>, _>>()?;
        graph
            .nodes
            .get_mut(&id)
            .unwrap()
            .properties
            .insert("childTypes".into(), json!(children));
    }
    Ok(())
}
