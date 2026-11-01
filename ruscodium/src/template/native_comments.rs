//! Bounded native LimeComment selection and Doxygen plain-text formatting.
use super::graph::{reference, Graph};
use serde_json::Value;
use std::collections::{BTreeMap, BTreeSet};

pub(super) type RawComments = BTreeMap<String, Vec<(String, String)>>;
const LIMIT: usize = 1024 * 1024;
const DEPTH: usize = 128;

pub(super) fn import(graph: &Graph, raw: &Value) -> Result<RawComments, String> {
    let map = raw.as_object().ok_or("raw_comments must be an object")?;
    let comments: BTreeSet<_> = graph
        .nodes
        .iter()
        .filter(|(_, n)| n.class == "com.here.gluecodium.model.lime.LimeComment")
        .map(|(id, _)| id.as_str())
        .collect();
    if map.keys().map(String::as_str).collect::<BTreeSet<_>>() != comments {
        return Err("raw_comments must contain exactly every LimeComment id".into());
    }
    let mut result = RawComments::new();
    for (id, value) in map {
        let mut sections = Vec::new();
        for entry in value
            .as_array()
            .ok_or("raw comment sections must be an array")?
        {
            let pair = entry
                .as_array()
                .filter(|a| a.len() == 2)
                .ok_or("raw comment section must be a pair")?;
            let tag = pair[0].as_str().ok_or("raw comment tag must be a string")?;
            let text = pair[1]
                .as_str()
                .ok_or("raw comment text must be a string")?;
            if tag.len() > LIMIT || text.len() > LIMIT {
                return Err("raw comment size limit exceeded".into());
            }
            sections.push((tag.to_owned(), text.to_owned()));
        }
        result.insert(id.clone(), sections);
    }
    // Validate all placeholder edges, including unused entries.
    for id in result.keys() {
        let node = &graph.nodes[id];
        let placeholders = node
            .properties
            .get("placeholders")
            .and_then(Value::as_object)
            .ok_or("invalid comment placeholders")?;
        for target in placeholders.values() {
            let target = reference(target).ok_or("invalid comment placeholder reference")?;
            if !result.contains_key(target) {
                return Err("invalid comment placeholder target".into());
            }
        }
        for (tag, name) in &result[id] {
            if tag == "Placeholder" && !placeholders.contains_key(name) {
                return Err("missing comment placeholder".into());
            }
        }
    }
    fn check(
        id: &str,
        graph: &Graph,
        active: &mut BTreeSet<String>,
        heights: &mut BTreeMap<String, usize>,
    ) -> Result<usize, String> {
        if let Some(height) = heights.get(id) {
            return Ok(*height);
        }
        if active.len() >= DEPTH || !active.insert(id.into()) {
            return Err("cyclic or too deep comment placeholders".into());
        }
        let mut height = 1;
        for value in graph.nodes[id].properties["placeholders"]
            .as_object()
            .unwrap()
            .values()
        {
            height = height.max(1 + check(reference(value).unwrap(), graph, active, heights)?);
        }
        active.remove(id);
        if height > DEPTH {
            return Err("cyclic or too deep comment placeholders".into());
        }
        heights.insert(id.into(), height);
        Ok(height)
    }
    let mut heights = BTreeMap::new();
    for id in result.keys() {
        check(id, graph, &mut BTreeSet::new(), &mut heights)?;
    }
    Ok(result)
}

fn kotlin_space(c: char) -> bool {
    (c.is_whitespace() && c != '\u{85}') || ('\u{1c}'..='\u{1f}').contains(&c)
}
fn trim(s: &str) -> &str {
    s.trim_matches(kotlin_space)
}

pub(crate) fn selected(graph: &Graph, value: &Value) -> Result<Option<String>, String> {
    let Some(raw) = &graph.raw_comments else {
        return Ok(None);
    };
    let id = reference(value).ok_or("expected comment reference")?;
    fn expand(
        id: &str,
        graph: &Graph,
        raw: &RawComments,
        depth: usize,
        memo: &mut BTreeMap<String, String>,
    ) -> Result<String, String> {
        if depth >= DEPTH {
            return Err("comment placeholder depth exceeded".into());
        }
        if let Some(cached) = memo.get(id) {
            return Ok(cached.clone());
        }
        let mut out = String::new();
        let sections = raw.get(id).ok_or("missing raw comment")?;
        let placeholders = graph.nodes[id].properties["placeholders"]
            .as_object()
            .ok_or("invalid placeholders")?;
        for (tag, text) in sections {
            let part = if tag == "Placeholder" {
                let target = placeholders
                    .get(text)
                    .and_then(reference)
                    .ok_or("missing comment placeholder")?;
                expand(target, graph, raw, depth + 1, memo)?
            } else if tag.is_empty() || tag == "Cpp" {
                text.clone()
            } else {
                continue;
            };
            if out.len().saturating_add(part.len()) > LIMIT {
                return Err("comment expansion size limit exceeded".into());
            }
            out.push_str(&part);
        }
        let result = trim(&out).to_owned();
        memo.insert(id.to_owned(), result.clone());
        Ok(result)
    }
    expand(id, graph, raw, 0, &mut BTreeMap::new()).map(Some)
}

pub(crate) fn format(text: &str) -> Result<String, String> {
    let text = trim(text);
    if text.contains("*/")
        || text.chars().any(|c| {
            matches!(
                c,
                '*' | '_' | '[' | ']' | '`' | '<' | '>' | '#' | '~' | '\\' | '|' | '{' | '}' | '&'
            ) || (c.is_control() && c != '\n' && c != '\t')
        })
    {
        return Err("unsupported C++ comment Markdown or control character".into());
    }
    let mut result = Vec::<String>::new();
    let mut pending_blank = false;
    let mut paragraph = false;
    for line in text.split('\n') {
        if line.trim_matches([' ', '\t']).is_empty() {
            if result
                .last()
                .is_some_and(|previous| previous.ends_with("  "))
            {
                return Err("unsupported paragraph-final hard break".into());
            }
            pending_blank = paragraph;
            continue;
        }
        let leading = line.len() - line.trim_start_matches([' ', '\t']).len();
        if !paragraph || pending_blank {
            if leading >= 4 || line[..leading].contains('\t') {
                return Err("unsupported C++ comment indented code".into());
            }
            if pending_blank {
                result.push(String::new());
            }
        }
        let line = line.trim_start_matches([' ', '\t']);
        let marker = line.trim_end_matches([' ', '\t']);
        if line
            .chars()
            .next()
            .is_some_and(|c| c == '-' || c == '+' || c == '=')
            && line.chars().nth(1).is_some_and(|c| c == ' ' || c == '\t')
            || marker == "+"
            || marker.chars().all(|c| c == '-')
            || marker.chars().all(|c| c == '=')
            || marker.split_once(['.', ')']).is_some_and(|(a, b)| {
                !a.is_empty()
                    && a.bytes().all(|x| x.is_ascii_digit())
                    && (b.is_empty() || b.starts_with([' ', '\t']))
            })
        {
            return Err("unsupported C++ comment list or heading".into());
        }
        let suffix = &line[line.trim_end_matches([' ', '\t']).len()..];
        if suffix.contains('\t') {
            return Err("unsupported C++ comment trailing tab".into());
        }
        let trailing = line.len() - line.trim_end_matches(' ').len();
        let line = if trailing == 1 {
            &line[..line.len() - 1]
        } else {
            line
        };
        result.push(line.to_owned());
        paragraph = true;
        pending_blank = false;
    }
    Ok(result.join("\n"))
}

#[cfg(test)]
mod tests {
    use super::{format, kotlin_space, selected};
    use crate::template::Graph;
    use serde_json::json;
    #[test]
    fn global_emptiness_differs_from_selected_platform_text() {
        let snapshot = json!({"schema":"gluecodium.reference-model.snapshot","version":1,"root":{"$ref":"c"},"nodes":[{"id":"c","class":"com.here.gluecodium.model.lime.LimeComment","properties":{"isExcluded":false,"placeholders":{}}}]});
        let mut graph = Graph::import(Some(&snapshot), None).unwrap();
        graph
            .attach_raw_comments(&json!({"c":[["Java","other platform"]]}))
            .unwrap();
        assert_eq!(
            graph.property(&json!({"$ref":"c"}), "isEmpty").unwrap(),
            Some(json!(false))
        );
        assert_eq!(
            selected(&graph, &json!({"$ref":"c"})).unwrap(),
            Some(String::new())
        );
    }
    #[test]
    fn expanded_placeholder_size_is_bounded() {
        let mut nodes = Vec::new();
        let mut raw = serde_json::Map::new();
        for index in 0..22 {
            let id = format!("n{index}");
            let placeholders = if index < 21 {
                json!({"next":{"$ref":format!("n{}", index + 1)}})
            } else {
                json!({})
            };
            nodes.push(json!({"id":id,"class":"com.here.gluecodium.model.lime.LimeComment","properties":{"placeholders":placeholders}}));
            raw.insert(
                id,
                if index < 21 {
                    json!([["Placeholder", "next"], ["Placeholder", "next"]])
                } else {
                    json!([["", "a"]])
                },
            );
        }
        let snapshot = json!({"schema":"gluecodium.reference-model.snapshot","version":1,"root":{"$ref":"n0"},"nodes":nodes});
        let mut graph = Graph::import(Some(&snapshot), None).unwrap();
        graph.attach_raw_comments(&raw.into()).unwrap();
        assert!(selected(&graph, &json!({"$ref":"n0"}))
            .unwrap_err()
            .contains("size limit"));
    }
    #[test]
    fn jvm_measured_plain_text_format_and_guards() {
        assert_eq!(
            format(" hello  world\n indented\n\n\nnext ").unwrap(),
            "hello  world\nindented\n\nnext"
        );
        assert_eq!(format("one \ntwo  \nthree").unwrap(), "one\ntwo  \nthree");
        assert_eq!(
            format("Bonjour café 中文\n\u{a0}continuation").unwrap(),
            "Bonjour café 中文\n\u{a0}continuation"
        );
        for text in [
            "prefix\n-- \nend",
            "prefix\na\t  \nend",
            "hello  \n\nworld",
            "+\n  a",
            "1.\n  a",
            "hello\n\n \tworld",
            "hello\n---",
            "hello\n===",
            "-\tentry",
            "1.\tentry",
            "1) entry",
            "hello\t \nworld",
            "[reference]",
            "**bold**",
            "before\n\n    code",
        ] {
            assert!(format(text).is_err(), "{text:?}");
        }
        assert!(kotlin_space('\u{a0}'));
        assert!(kotlin_space('\u{1c}'));
        assert!(!kotlin_space('\u{85}'));
    }
}
