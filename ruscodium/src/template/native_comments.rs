//! Native LimeComment selection and Doxygen Markdown formatting.
use super::graph::{reference, Graph};
use pulldown_cmark::{BrokenLink, Event, LinkType, Options, Parser, Tag};
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

/// An unresolved documentation reference encountered while rendering.
#[derive(Clone, Debug, Eq, Ord, PartialEq, PartialOrd)]
pub struct DocWarning {
    pub scope: String,
    pub message: String,
}

pub(crate) fn format(text: &str) -> Result<String, String> {
    format_with_references(text, "", &BTreeMap::new(), false)
}

pub(crate) fn format_with_references(
    text: &str,
    scope: &str,
    names: &BTreeMap<String, String>,
    werror: bool,
) -> Result<String, String> {
    format_with_diagnostics(text, scope, names, werror).map(|(text, _)| text)
}

/// Resolve links against the model and return warnings to the rendering caller.
pub(crate) fn format_with_diagnostics(
    text: &str,
    scope: &str,
    names: &BTreeMap<String, String>,
    werror: bool,
) -> Result<(String, Vec<DocWarning>), String> {
    let text = trim(text);
    let path: Vec<_> = if scope.is_empty() {
        Vec::new()
    } else {
        scope.split('.').collect()
    };
    let mut replacements = Vec::new();
    let mut missing = Vec::new();
    let mut callback = |link: BrokenLink<'_>| {
        if link.span.start > 0 && text.as_bytes()[link.span.start - 1] == b'!' {
            return None;
        }
        let raw = link.reference.as_ref();
        let mut normalized = raw.replace(' ', "");
        if let Some((name, signature)) = normalized.split_once('(') {
            let signature = signature.replace('(', "");
            normalized = format!(
                "{}({}",
                name,
                signature
                    .split(',')
                    .map(|x| x.rsplit('.').next().unwrap_or(x))
                    .collect::<Vec<_>>()
                    .join(",")
            );
        }
        let target = (0..=path.len()).rev().find_map(|i| {
            let mut key = path[..i].join(".");
            if !key.is_empty() {
                key.push('.');
            }
            key.push_str(&normalized);
            names.get(&key)
        });
        if let Some(target) = target {
            let original = &text[link.span.clone()];
            let prefix = match link.link_type {
                LinkType::Reference | LinkType::ReferenceUnknown => original
                    .find("][")
                    .map(|i| &original[..i + 1])
                    .unwrap_or(""),
                _ => "",
            };
            replacements.push((link.span, format!("{prefix}{target}")));
            Some(("".into(), "".into()))
        } else {
            missing.push(raw.to_owned());
            None
        }
    };
    for _ in Parser::new_with_broken_link_callback(text, Options::empty(), Some(&mut callback)) {}
    if werror && !missing.is_empty() {
        return Err(format!(
            "Failed to resolve documentation reference [{}]",
            missing[0]
        ));
    }
    let mut rewritten = text.to_owned();
    replacements.sort_by_key(|(range, _)| range.start);
    for (range, value) in replacements.into_iter().rev() {
        rewritten.replace_range(range, &value);
    }
    rewritten = normalize_block_boundaries(&rewritten);
    rewritten = normalize_refdefs(&normalize_quotes(&normalize_misc(&normalize_loose_lists(
        &normalize_blocks(&rewritten),
    ))));

    rewritten = normalize_list_leading_blocks(&rewritten);
    let diagnostics = missing
        .into_iter()
        .map(|name| DocWarning {
            scope: scope.to_owned(),
            message: format!("Failed to resolve documentation reference [{name}]"),
        })
        .collect();
    Ok((trim(&rewritten).to_owned(), diagnostics))
}

fn normalize_block_boundaries(input: &str) -> String {
    let mut rewritten = input.to_owned();
    let mut boundaries = Vec::new();
    let mut depth = 0usize;
    let mut previous_list = false;
    let definitions: Vec<_> = Parser::new(&rewritten)
        .reference_definitions()
        .iter()
        .map(|(_, def)| def.span.clone())
        .collect();
    for (event, range) in Parser::new(&rewritten).into_offset_iter() {
        match event {
            Event::Start(tag) => {
                let immediately_after_definition = definitions.iter().any(|definition| {
                    definition.end <= range.start
                        && rewritten[definition.end..range.start].trim().is_empty()
                        && rewritten[definition.end..range.start].matches('\n').count() == 1
                });
                if depth == 0 && previous_list && matches!(tag, Tag::List(_)) {
                    boundaries.push(range.start);
                }
                if depth == 0
                    && matches!(
                        tag,
                        Tag::Heading { .. }
                            | Tag::CodeBlock(pulldown_cmark::CodeBlockKind::Fenced(_))
                            | Tag::BlockQuote(_)
                    )
                {
                    if !immediately_after_definition || !matches!(tag, Tag::Heading { .. }) {
                        boundaries.push(range.start);
                    }
                    boundaries.push(range.end);
                }
                if depth == 0 && matches!(tag, Tag::Paragraph) && immediately_after_definition {
                    boundaries.push(range.start);
                }
                if depth == 0 && matches!(tag, Tag::HtmlBlock) {
                    let line_start = rewritten[..range.start].rfind('\n').map_or(0, |n| n + 1);
                    if line_start > 0 && !rewritten[..line_start].ends_with("\n\n") {
                        boundaries.push(range.start);
                    }
                    let html = rewritten[range.clone()].trim_end().to_ascii_lowercase();
                    if ["</pre>", "</script>", "</style>", "?>", "]]>"]
                        .iter()
                        .any(|end| html.ends_with(end))
                    {
                        boundaries.push(range.end);
                    }
                }
                if depth == 0 {
                    previous_list = false;
                }
                depth += 1;
            }
            Event::End(tag) => {
                depth = depth.saturating_sub(1);
                if depth == 0 {
                    previous_list = matches!(tag, pulldown_cmark::TagEnd::List(_));
                }
            }
            Event::Rule if depth == 0 => {
                previous_list = false;
                boundaries.push(range.start);
                boundaries.push(range.end);
            }
            _ => {}
        }
    }
    boundaries.sort_unstable();
    boundaries.dedup();
    for pos in boundaries.into_iter().rev() {
        let line_start = rewritten[..pos].rfind('\n').map_or(0, |n| n + 1);
        let before_pos = if rewritten[line_start..pos]
            .trim_matches([' ', '\t'])
            .is_empty()
        {
            line_start
        } else {
            pos
        };
        let before = rewritten[..before_pos].trim_end_matches('\n').len();
        let after = pos + rewritten[pos..].len() - rewritten[pos..].trim_start_matches('\n').len();
        if before > 0 && after < rewritten.len() {
            rewritten.replace_range(before..after, "\n\n");
        }
    }
    rewritten
}

/// Put a leading block on its own line inside a list item, and join a simple
/// continuation paragraph to an otherwise empty marker.
fn normalize_list_leading_blocks(text: &str) -> String {
    use pulldown_cmark::{CodeBlockKind, TagEnd};
    struct Item {
        marker_end: usize,
        indent: usize,
        first: bool,
    }
    let mut stack = Vec::new();
    let mut items: Vec<Option<Item>> = Vec::new();
    let mut edits = Vec::new();
    for (event, range) in Parser::new(text).into_offset_iter() {
        match event {
            Event::Start(tag) => {
                if matches!(tag, Tag::Item) {
                    let line_start = text[..range.start].rfind('\n').map_or(0, |n| n + 1);
                    let prefix = &text[line_start..range.start];
                    let candidate = if prefix.trim().is_empty() {
                        let line_end = text[range.start..]
                            .find('\n')
                            .map_or(text.len(), |n| range.start + n);
                        let line = &text[line_start..line_end];
                        let leading = line.len() - line.trim_start_matches([' ', '\t']).len();
                        let tail = &line[leading..];
                        let digits = tail.bytes().take_while(u8::is_ascii_digit).count();
                        let marker_len = if tail.starts_with(['-', '+', '*']) {
                            1
                        } else if digits > 0
                            && matches!(tail.as_bytes().get(digits), Some(b'.' | b')'))
                        {
                            digits + 1
                        } else {
                            0
                        };
                        (marker_len > 0).then_some(Item {
                            marker_end: line_start + leading + marker_len,
                            indent: leading + marker_len + 1,
                            first: true,
                        })
                    } else {
                        None
                    };
                    items.push(candidate);
                } else if stack.last() == Some(&TagEnd::Item) {
                    if let Some(Some(item)) = items.last_mut() {
                        if item.first {
                            item.first = false;
                            let block_indent = match &tag {
                                Tag::CodeBlock(CodeBlockKind::Indented) => Some(item.indent + 4),
                                Tag::CodeBlock(_) | Tag::Heading { .. } | Tag::HtmlBlock => {
                                    Some(item.indent)
                                }
                                _ => None,
                            };
                            if range.start >= item.marker_end {
                                let gap = &text[item.marker_end..range.start];
                                if gap.trim().is_empty() {
                                    if let Some(indent) = block_indent {
                                        let extra = if matches!(
                                            tag,
                                            Tag::CodeBlock(CodeBlockKind::Indented)
                                        ) {
                                            text[range.start..range.end]
                                                .bytes()
                                                .take_while(|b| *b == b' ')
                                                .count()
                                        } else {
                                            0
                                        };
                                        edits.push((
                                            item.marker_end..range.start + extra,
                                            format!(" \n\n{}", " ".repeat(indent)),
                                        ));
                                        if matches!(tag, Tag::Heading { .. } | Tag::HtmlBlock)
                                            && range.end < text.len()
                                            && !text[range.end..].starts_with('\n')
                                        {
                                            edits.push((range.end..range.end, "\n".into()));
                                        }
                                    } else if matches!(tag, Tag::Paragraph)
                                        && gap.matches('\n').count() == 1
                                    {
                                        edits.push((item.marker_end..range.start, " ".into()));
                                    }
                                }
                            }
                        }
                    }
                }
                stack.push(tag.to_end());
            }
            Event::Text(_) if stack.last() == Some(&TagEnd::Item) => {
                if let Some(Some(item)) = items.last_mut() {
                    if item.first && range.start >= item.marker_end {
                        item.first = false;
                        let gap = &text[item.marker_end..range.start];
                        if gap.trim().is_empty() && gap.matches('\n').count() == 1 {
                            edits.push((item.marker_end..range.start, " ".into()));
                        }
                    }
                }
            }
            Event::Rule if stack.last() == Some(&TagEnd::Item) => {
                if let Some(Some(item)) = items.last_mut() {
                    if item.first && range.start >= item.marker_end {
                        item.first = false;
                        let gap = &text[item.marker_end..range.start];
                        if gap.trim().is_empty() {
                            edits.push((
                                item.marker_end..range.start,
                                format!(" \n\n{}", " ".repeat(item.indent)),
                            ));
                        }
                    }
                }
            }
            Event::End(tag) => {
                if matches!(tag, TagEnd::Item) {
                    items.pop();
                }
                stack.pop();
            }
            _ => {}
        }
    }
    apply_edits(text, edits)
}

fn normalize_blocks(text: &str) -> String {
    struct List {
        indent: usize,
        next: Option<u64>,
        width: usize,
    }
    struct Item {
        range: std::ops::Range<usize>,
        line_start: usize,
        original_indent: usize,
        output_indent: usize,
    }
    let mut lists: Vec<List> = Vec::new();
    let mut items: Vec<Item> = Vec::new();
    let mut edits: Vec<(std::ops::Range<usize>, String)> = Vec::new();
    let inline_code: Vec<_> = Parser::new(text)
        .into_offset_iter()
        .filter_map(|(e, r)| matches!(e, Event::Code(_)).then_some(r))
        .collect();
    let mut marker_lines_with_indented_code = BTreeSet::new();
    let mut item_stack = Vec::new();
    for (event, range) in Parser::new(text).into_offset_iter() {
        match event {
            Event::Start(Tag::Item) => item_stack.push(range.start),
            Event::End(pulldown_cmark::TagEnd::Item) => {
                item_stack.pop();
            }
            Event::Start(Tag::CodeBlock(pulldown_cmark::CodeBlockKind::Indented)) => {
                if let Some(start) = item_stack.last() {
                    if !text[*start..range.start].contains('\n') {
                        marker_lines_with_indented_code
                            .insert(text[..*start].rfind('\n').map_or(0, |n| n + 1));
                    }
                }
            }
            _ => {}
        }
    }
    let code_blocks: Vec<_> = Parser::new(text)
        .into_offset_iter()
        .filter_map(|(event, range)| match event {
            Event::Start(Tag::CodeBlock(pulldown_cmark::CodeBlockKind::Indented)) => {
                let leading = text[range.clone()]
                    .bytes()
                    .take_while(|b| *b == b' ')
                    .count();
                Some((range, Some(leading)))
            }
            Event::Start(Tag::CodeBlock(pulldown_cmark::CodeBlockKind::Fenced(_))) => {
                Some((range, None))
            }
            _ => None,
        })
        .collect();
    for (event, range) in Parser::new(text).into_offset_iter() {
        match event {
            Event::Start(Tag::Paragraph) if lists.is_empty() => {
                let start = text[..range.start].rfind('\n').map_or(0, |n| n + 1);
                let mut line_start = start;
                for line in text[start..range.end].split_inclusive('\n') {
                    let body = line.strip_suffix('\n').unwrap_or(line);
                    let left = body.len() - body.trim_start_matches([' ', '\t']).len();
                    if !body.trim().is_empty() && !body[left..].starts_with('>') {
                        let after_open_bracket = line_start > 0
                            && text[..line_start]
                                .trim_end_matches('\n')
                                .rsplit('\n')
                                .next()
                                == Some("[")
                            && body[left..].starts_with(']');
                        if left > 0
                            && !after_open_bracket
                            && !inline_code
                                .iter()
                                .any(|r| r.start < line_start + left && line_start < r.end)
                        {
                            edits.push((line_start..line_start + left, String::new()));
                        }
                        let trailing = body.len() - body.trim_end_matches(' ').len();
                        if trailing == 1
                            && !inline_code.iter().any(|r| {
                                r.start < line_start + body.len()
                                    && line_start + body.len() - 1 < r.end
                            })
                        {
                            edits.push((
                                line_start + body.len() - 1..line_start + body.len(),
                                String::new(),
                            ));
                        }
                    }
                    line_start += line.len();
                }
            }
            Event::Start(Tag::List(first)) => {
                let indent = lists.last().map_or(0, |l| l.indent + l.width);
                lists.push(List {
                    indent,
                    next: first,
                    width: 2,
                });
            }
            Event::End(pulldown_cmark::TagEnd::List(_)) => {
                lists.pop();
            }
            Event::Start(Tag::Item) => {
                let line_start = text[..range.start].rfind('\n').map_or(0, |n| n + 1);
                let nested_on_line = !text[line_start..range.start].trim().is_empty();
                let start = if nested_on_line {
                    range.start
                } else {
                    line_start
                };
                let line_end = text[range.start..]
                    .find('\n')
                    .map_or(text.len(), |n| range.start + n);
                let line = &text[start..line_end];
                let leading = line.len() - line.trim_start_matches([' ', '\t']).len();
                let tail = &line[leading..];
                let marker_len = if tail.starts_with(['-', '+', '*']) {
                    1
                } else {
                    let digits = tail.bytes().take_while(u8::is_ascii_digit).count();
                    if digits > 0 && matches!(tail.as_bytes().get(digits), Some(b'.' | b')')) {
                        digits + 1
                    } else {
                        0
                    }
                };
                if marker_len == 0 {
                    continue;
                }
                let after = &tail[marker_len..];
                let spaces = after.len() - after.trim_start_matches([' ', '\t']).len();
                if let Some(list) = lists.last_mut() {
                    let marker = if let Some(number) = list.next.as_mut() {
                        let m = format!("{}{}", *number, tail.as_bytes()[marker_len - 1] as char);
                        *number += 1;
                        m
                    } else {
                        tail[..marker_len].to_owned()
                    };
                    list.width = marker.len() + 1;
                    let suffix = " ";
                    let original_indent = text[line_start..start + leading + marker_len + spaces]
                        .chars()
                        .fold(0, |col, ch| {
                            if ch == '\t' {
                                (col / 4 + 1) * 4
                            } else {
                                col + 1
                            }
                        })
                        + usize::from(spaces == 0);
                    items.push(Item {
                        range: range.clone(),
                        line_start,
                        original_indent,
                        output_indent: list.indent + list.width,
                    });
                    let indent = if nested_on_line {
                        String::new()
                    } else {
                        " ".repeat(list.indent)
                    };
                    if !marker_lines_with_indented_code.contains(&line_start) {
                        edits.push((
                            start..start + leading + marker_len + spaces,
                            format!("{indent}{marker}{suffix}"),
                        ));
                    }
                }
            }
            Event::Start(Tag::BlockQuote(_)) if !lists.is_empty() => {
                let start = text[..range.start].rfind('\n').map_or(0, |n| n + 1);
                if start > 0
                    && text[start..range.start].trim().is_empty()
                    && !text[..start].ends_with("\n\n")
                {
                    edits.push((start..start, "\n".into()));
                }
            }
            _ => {}
        }
    }
    let item_lines: BTreeSet<_> = items.iter().map(|x| x.line_start).collect();
    let mut at = 0;
    for line in text.split_inclusive('\n') {
        if !item_lines.contains(&at) && !line.trim().is_empty() {
            if let Some(item) = items
                .iter()
                .filter(|x| x.line_start < at && at < x.range.end)
                .max_by_key(|x| x.range.start)
            {
                let count = line
                    .bytes()
                    .take_while(|b| *b == b' ' || *b == b'\t')
                    .count();
                let original = line[..count].chars().fold(0usize, |col, ch| {
                    if ch == '\t' {
                        (col / 4 + 1) * 4
                    } else {
                        col + 1
                    }
                });
                let block = code_blocks
                    .iter()
                    .find(|(r, _)| r.start < at + line.len() && at < r.end);
                let output = match block {
                    Some((_, Some(extra))) => {
                        item.output_indent
                            + 4
                            + original.saturating_sub(item.original_indent + 4 + extra)
                    }
                    Some((_, None)) => {
                        original.saturating_sub(item.original_indent) + item.output_indent
                    }
                    None => item.output_indent,
                };
                if line[..count] != " ".repeat(output)
                    && !inline_code
                        .iter()
                        .any(|r| r.start < at + count && at < r.end)
                {
                    edits.push((at..at + count, " ".repeat(output)));
                }
            }
        }
        at += line.len();
    }
    apply_edits(text, edits)
}

fn apply_edits(text: &str, mut edits: Vec<(std::ops::Range<usize>, String)>) -> String {
    edits.sort_by_key(|(r, _)| (r.start, r.end));
    let mut result = text.to_owned();
    for (range, value) in edits.into_iter().rev() {
        result.replace_range(range, &value);
    }
    result
}

fn normalize_refdefs(text: &str) -> String {
    let parser = Parser::new(text);
    let mut edits = Vec::new();
    for (_, definition) in parser.reference_definitions().iter() {
        let range = definition.span.clone();
        let line_start = text[..range.start].rfind('\n').map_or(0, |n| n + 1);
        if !text[line_start..range.start]
            .trim_matches([' ', '\t'])
            .is_empty()
        {
            continue;
        }
        let mut at = range.start;
        for (index, line) in text[range.clone()].split_inclusive('\n').enumerate() {
            if index > 0 {
                let leading = line.len() - line.trim_start_matches([' ', '\t']).len();
                if leading > 0 {
                    edits.push((at..at + leading, String::new()));
                }
            }
            at += line.len();
        }
        let last = &text[range.clone()];
        let trailing = last.len() - last.trim_end_matches([' ', '\t']).len();
        if trailing > 0 {
            edits.push((range.end - trailing..range.end, String::new()));
        }
        let after = &text[range.end..];
        let trailing = after
            .bytes()
            .take_while(|b| *b == b' ' || *b == b'\t')
            .count();
        if trailing > 0
            && (range.end + trailing == text.len() || after[trailing..].starts_with('\n'))
        {
            edits.push((range.end..range.end + trailing, String::new()));
        }
    }
    // Flexmark groups consecutive reference definitions, including repeated
    // labels. Pulldown's reference map keeps only the first definition.
    let protected: Vec<_> = Parser::new(text)
        .into_offset_iter()
        .filter_map(|(event, range)| {
            matches!(event, Event::Start(Tag::CodeBlock(_) | Tag::HtmlBlock)).then_some(range)
        })
        .collect();
    let mut at = 0;
    let mut previous: Option<usize> = None;
    for line in text.split_inclusive('\n') {
        let body = line.trim();
        if body.is_empty() {
            at += line.len();
            continue;
        }
        let label = body.strip_prefix('[').and_then(|s| s.split_once("]:"));
        let definition = !protected
            .iter()
            .any(|range| range.start <= at && at < range.end)
            && label.is_some_and(|(name, _)| parser.reference_definitions().get(name).is_some());
        if definition {
            if let Some(end) = previous {
                if text[end..at].matches('\n').count() > 1 {
                    edits.push((end..at, "\n".into()));
                }
            }
            previous = Some(at + line.trim_end_matches('\n').len());
        } else {
            previous = None;
        }
        at += line.len();
    }
    apply_edits(text, edits)
}
/// Reproduce Flexmark's separation of loose list items and nested lists.
fn normalize_loose_lists(text: &str) -> String {
    use pulldown_cmark::TagEnd;
    #[derive(Default)]
    struct Item {
        start: usize,
        nested: Vec<usize>,
        ends_in_list: bool,
        loose_child: bool,
    }
    #[derive(Default)]
    struct List {
        loose: bool,
        nested: bool,
        items: Vec<Item>,
    }
    let mut stack = Vec::new();
    let mut active: Vec<List> = Vec::new();
    let mut lists = Vec::new();
    for (event, range) in Parser::new(text).into_offset_iter() {
        match event {
            Event::Start(tag) => {
                match &tag {
                    Tag::List(_) => {
                        if stack.last() == Some(&TagEnd::Item) {
                            if let Some(parent) = active.last_mut() {
                                parent.nested = true;
                                if let Some(item) = parent.items.last_mut() {
                                    item.nested
                                        .push(text[..range.start].rfind('\n').map_or(0, |n| n + 1));
                                    item.ends_in_list = true;
                                }
                            }
                        }
                        active.push(List::default());
                    }
                    Tag::Item => {
                        if let Some(list) = active.last_mut() {
                            list.items.push(Item {
                                start: text[..range.start].rfind('\n').map_or(0, |n| n + 1),
                                ..Item::default()
                            });
                        }
                    }
                    Tag::Paragraph if stack.last() == Some(&TagEnd::Item) => {
                        if let Some(list) = active.last_mut() {
                            list.loose = true;
                            if let Some(item) = list.items.last_mut() {
                                item.ends_in_list = false;
                            }
                        }
                    }
                    Tag::BlockQuote(_) | Tag::CodeBlock(_) | Tag::HtmlBlock
                        if stack.last() == Some(&TagEnd::Item) =>
                    {
                        if let Some(list) = active.last_mut() {
                            list.nested = true;
                            if let Some(item) = list.items.last_mut() {
                                item.ends_in_list = false;
                            }
                        }
                    }
                    _ => {}
                }
                stack.push(tag.to_end());
            }
            Event::Text(_) if stack.last() == Some(&TagEnd::Item) => {
                if let Some(item) = active.last_mut().and_then(|list| list.items.last_mut()) {
                    item.ends_in_list = false;
                }
            }
            Event::End(tag) => {
                if matches!(tag, TagEnd::List(_)) {
                    if let Some(list) = active.pop() {
                        if let Some(item) =
                            active.last_mut().and_then(|parent| parent.items.last_mut())
                        {
                            if item.ends_in_list {
                                item.loose_child |= list.loose;
                            }
                        }
                        lists.push(list);
                    }
                }
                stack.pop();
            }
            _ => {}
        }
    }
    let mut insertions = BTreeSet::new();
    let mut removals = BTreeSet::new();
    for list in lists {
        if list.loose && list.nested {
            for item in &list.items {
                for &position in &item.nested {
                    if position > item.start && !text[..position].ends_with("\n\n") {
                        insertions.insert(position);
                    }
                }
            }
        }
        for pair in list.items.windows(2) {
            let (before, after) = (&pair[0], &pair[1]);
            let position = after.start;
            if position == 0 {
                continue;
            }
            if list.loose && before.ends_in_list {
                let start = text[..position].trim_end_matches('\n').len();
                if position - start > 1 {
                    removals.insert((start, position));
                }
            } else if (list.loose && !list.nested) || (!list.loose && before.loose_child) {
                if !text[..position].ends_with("\n\n") {
                    insertions.insert(position);
                }
            }
        }
    }
    let mut edits: Vec<_> = removals
        .into_iter()
        .map(|(start, end)| (start..end, "\n".into()))
        .collect();
    edits.extend(insertions.into_iter().map(|pos| (pos..pos, "\n".into())));
    apply_edits(text, edits)
}

fn normalize_misc(text: &str) -> String {
    use pulldown_cmark::CodeBlockKind;
    let mut edits: Vec<(std::ops::Range<usize>, String)> = Vec::new();
    let mut protected = Vec::new();
    let mut indented_code = Vec::new();
    let mut quotes = Vec::new();
    let mut quote_depth = 0usize;
    let mut list_depth = 0usize;
    for (event, range) in Parser::new(text).into_offset_iter() {
        match event {
            Event::Start(Tag::List(_)) => list_depth += 1,
            Event::End(pulldown_cmark::TagEnd::List(_)) => {
                list_depth = list_depth.saturating_sub(1);
            }
            Event::Start(Tag::BlockQuote(_)) => {
                if quote_depth == 0 {
                    quotes.push(range);
                }
                quote_depth += 1;
            }
            Event::End(pulldown_cmark::TagEnd::BlockQuote(_)) => {
                quote_depth = quote_depth.saturating_sub(1)
            }
            Event::Start(Tag::CodeBlock(kind)) => {
                protected.push(range.clone());
                if matches!(kind, CodeBlockKind::Indented) && list_depth == 0 && quote_depth == 0 {
                    indented_code.push(range.clone());
                    let block = &text[range.clone()];
                    let extra = block.bytes().take_while(|b| *b == b' ').count();
                    if extra > 0 {
                        let mut at = text[..range.start].rfind('\n').map_or(0, |n| n + 1);
                        for line in text[at..range.end].split_inclusive('\n') {
                            if !line.trim().is_empty() {
                                let leading = line.bytes().take_while(|b| *b == b' ').count();
                                let remove = extra.min(leading.saturating_sub(4));
                                if remove > 0 {
                                    edits.push((at..at + remove, String::new()));
                                }
                            }
                            at += line.len();
                        }
                    }
                }
                if matches!(kind, CodeBlockKind::Fenced(_)) && list_depth == 0 {
                    let block = &text[range.clone()];
                    let lines: Vec<_> = block.split_inclusive('\n').collect();
                    let line_start = text[..range.start].rfind('\n').map_or(0, |n| n + 1);
                    if !lines.is_empty()
                        && text[line_start..range.start]
                            .trim_matches([' ', '\t'])
                            .is_empty()
                        && lines[0].trim_start().starts_with(['`', '~'])
                    {
                        let open = lines[0].trim_end_matches('\n');
                        let spaces = open.len() - open.trim_start_matches(' ').len();
                        let ch = open.as_bytes()[spaces];
                        let marker_len = open[spaces..].bytes().take_while(|b| *b == ch).count();
                        let marker = (ch as char).to_string().repeat(marker_len);
                        let info = &open[spaces + marker_len..];
                        let info_spaces = info.len() - info.trim_start_matches([' ', '\t']).len();
                        if spaces + info_spaces > 0 {
                            edits.push((
                                range.start..range.start + spaces + marker_len + info_spaces,
                                marker.clone(),
                            ));
                        }
                        let last = lines.last().unwrap().trim_end_matches('\n');
                        let last_trim = last.trim_start_matches(' ');
                        let indentation = last.len() - last_trim.len();
                        let fence_len = last_trim.bytes().take_while(|b| *b == ch).count();
                        let closed = lines.len() > 1
                            && indentation <= 3
                            && fence_len >= marker_len
                            && last_trim[fence_len..].trim().is_empty();
                        let content_end = lines.len() - usize::from(closed);
                        let content = &lines[1..content_end];
                        let indent = content
                            .iter()
                            .filter(|line| !line.trim().is_empty())
                            .map(|line| line.bytes().take_while(|c| *c == b' ').count())
                            .min()
                            .unwrap_or(0);
                        if indent > 0 {
                            let mut at = range.start + lines[0].len();
                            for line in content {
                                let count =
                                    line.bytes().take_while(|c| *c == b' ').count().min(indent);
                                if count > 0 {
                                    edits.push((at..at + count, String::new()));
                                }
                                at += line.len();
                            }
                        }
                        if closed {
                            let at = range.end - lines.last().unwrap().len();
                            edits.push((at..at + last.len(), marker));
                        } else {
                            let prefix = if block.ends_with('\n') { "" } else { "\n" };
                            let suffix = if range.end < text.len() { "\n" } else { "" };
                            edits.push((range.end..range.end, format!("{prefix}{marker}{suffix}")));
                        }
                    }
                }
            }
            Event::Start(Tag::HtmlBlock) => {
                protected.push(range.clone());
                let html = &text[range.clone()];
                if html.starts_with("<!--") {
                    let mut at = range.start;
                    for (index, line) in html.split_inclusive('\n').enumerate() {
                        if index > 0 {
                            let leading = line.len() - line.trim_start_matches([' ', '\t']).len();
                            if leading > 0 {
                                edits.push((at..at + leading, String::new()));
                            }
                        }
                        if let Some(close) = line.find("-->") {
                            let end = line.trim_end_matches('\n').len();
                            if close + 3 < end {
                                let replace = line[..end]
                                    .char_indices()
                                    .rev()
                                    .nth(2)
                                    .map(|(i, _)| i)
                                    .unwrap_or(0);
                                edits.push((at + replace..at + end, "-->".into()));
                            }
                        }
                        at += line.len();
                    }
                }
            }
            Event::Start(
                Tag::Link {
                    link_type: LinkType::Inline,
                    ..
                }
                | Tag::Image {
                    link_type: LinkType::Inline,
                    ..
                },
            ) => {
                let source = &text[range.clone()];
                if (source.starts_with('[') || source.starts_with("![")) && source.ends_with(')') {
                    if let Some(split) = source.find("](") {
                        let image = source.starts_with('!');
                        let label = source[usize::from(image) + 1..split]
                            .trim_matches([' ', '\t', '\n', '\r']);
                        let inner = source[split + 2..source.len() - 1]
                            .trim_matches([' ', '\t', '\n', '\r']);
                        let mut parts = inner.splitn(2, [' ', '\t', '\n', '\r']);
                        let url = parts.next().unwrap_or("");
                        let suffix = parts
                            .next()
                            .map(|s| s.trim_start_matches([' ', '\t', '\n', '\r']))
                            .filter(|s| !s.is_empty());
                        let image_prefix = if image { "!" } else { "" };
                        let extra_angle = if image && url.starts_with('<') {
                            "<"
                        } else {
                            ""
                        };
                        let formatted = match suffix {
                            Some(suffix) => {
                                format!("{image_prefix}[{label}]({extra_angle}{url} {suffix})")
                            }
                            None => format!("{image_prefix}[{label}]({extra_angle}{url})"),
                        };
                        if formatted != source {
                            edits.push((range, formatted));
                        }
                    }
                }
            }
            Event::Start(Tag::Heading { .. }) => {
                let heading = &text[range.clone()];
                let lines: Vec<_> = heading.lines().collect();
                if lines.len() > 2 {
                    let last = lines.last().unwrap().trim();
                    if !last.is_empty()
                        && (last.bytes().all(|c| c == b'-') || last.bytes().all(|c| c == b'='))
                    {
                        let mut at = range.start;
                        for line in &lines[..lines.len() - 1] {
                            let end = line.trim_end_matches([' ', '\t']).len();
                            if end < line.len() {
                                edits.push((at + end..at + line.len(), String::new()));
                            }
                            at += line.len() + 1;
                        }
                    }
                } else if let [first, last] = lines.as_slice() {
                    let marker = last.trim();
                    if !marker.is_empty()
                        && (marker.bytes().all(|c| c == b'-') || marker.bytes().all(|c| c == b'='))
                    {
                        let at = range.start + first.len() + 1;
                        let end = first.trim_end_matches([' ', '\t']).len();
                        if end < first.len() {
                            edits.push((
                                range.start + end..range.start + first.len(),
                                String::new(),
                            ));
                        }
                        edits.push((
                            at..at + last.len(),
                            format!(
                                "{}{}",
                                if list_depth > 0 {
                                    &last[..last.len() - last.trim_start_matches([' ', '\t']).len()]
                                } else {
                                    ""
                                },
                                (marker.as_bytes()[0] as char)
                                    .to_string()
                                    .repeat(first.trim().chars().count().max(3)),
                            ),
                        ));
                    }
                } else if let Some(first) = heading.lines().next() {
                    if first.starts_with('#') && !first.contains('[') {
                        let open = first.bytes().take_while(|c| *c == b'#').count();
                        let tail = first[open..].trim_matches([' ', '\t']);
                        let closing = tail.len() - tail.trim_end_matches('#').len();
                        let body = &tail[..tail.len() - closing];
                        let has_close =
                            closing > 0 && (body.is_empty() || body.ends_with([' ', '\t']));
                        let formatted = if has_close {
                            format!(
                                "{} {} {}",
                                &first[..open],
                                body.trim_end_matches([' ', '\t']),
                                "#".repeat(closing)
                            )
                        } else {
                            format!("{} {}", &first[..open], tail)
                        };
                        if formatted != first {
                            edits.push((range.start..range.start + first.len(), formatted));
                        }
                    }
                }
            }
            _ => {}
        }
    }
    for range in quotes {
        let start = text[..range.start].rfind('\n').map_or(0, |n| n + 1);
        let mut at = start;
        for line in text[start..range.end].split_inclusive('\n') {
            let end = at + line.len();
            if !protected.iter().any(|r| r.start < end && at < r.end) {
                let mut pos = line.len() - line.trim_start_matches([' ', '\t']).len();
                while line.as_bytes().get(pos) == Some(&b'>') {
                    let after = pos + 1;
                    let count = line[after..]
                        .bytes()
                        .take_while(|b| *b == b' ' || *b == b'\t')
                        .count();
                    let remaining = &line[after + count..];
                    if count < 5 {
                        let wanted = if remaining.is_empty() || remaining == "\n" {
                            ""
                        } else {
                            " "
                        };
                        if &line[after..after + count] != wanted {
                            edits.push((at + after..at + after + count, wanted.into()));
                        }
                    }
                    pos = after + count;
                }
            }
            at = end;
        }
    }
    let mut at = 0;
    let mut blank = false;
    for line in text.split_inclusive('\n') {
        let in_protected = protected.iter().any(|r| r.start <= at && at < r.end);
        let in_indented_code = indented_code
            .iter()
            .any(|r| r.start < at + line.len() && at < r.end);
        if in_indented_code && line.trim().is_empty() && line.ends_with('\n') && line != "\n" {
            edits.push((at..at + line.len(), "\n".into()));
            blank = false;
        } else if !in_protected && line.trim().is_empty() {
            if blank {
                edits.push((at..at + line.len(), String::new()));
            } else if line.ends_with('\n') && line != "\n" {
                edits.push((at..at + line.len(), "\n".into()));
            }
            blank = true;
        } else {
            blank = false;
        }
        at += line.len();
    }
    apply_edits(text, edits)
}
fn normalize_quotes(text: &str) -> String {
    let mut ranges = Vec::new();
    let mut code = Vec::new();
    let mut headings = Vec::new();
    let mut depth = 0usize;
    let mut list_depth = 0usize;
    let mut outside_list_depth = 0usize;
    for (event, range) in Parser::new(text).into_offset_iter() {
        match event {
            Event::Start(Tag::List(_)) => list_depth += 1,
            Event::End(pulldown_cmark::TagEnd::List(_)) => {
                list_depth = list_depth.saturating_sub(1)
            }
            Event::Start(Tag::BlockQuote(_)) => {
                depth += 1;
                if depth == 1 && list_depth == 0 {
                    outside_list_depth = depth;
                }
                if outside_list_depth != 0 {
                    ranges.push((range, depth));
                }
            }
            Event::End(pulldown_cmark::TagEnd::BlockQuote(_)) => {
                if depth == 1 {
                    outside_list_depth = 0;
                }
                depth = depth.saturating_sub(1);
            }
            Event::Start(Tag::Heading { .. }) if outside_list_depth != 0 => {
                headings.push((range, depth))
            }
            Event::Start(Tag::CodeBlock(_)) if outside_list_depth != 0 => code.push((range, depth)),
            _ => {}
        }
    }
    if ranges.is_empty() {
        return text.to_owned();
    }
    let roots: Vec<_> = ranges
        .iter()
        .filter(|(_, depth)| *depth == 1)
        .map(|(r, _)| r.clone())
        .collect();
    let mut edits = Vec::new();
    for root in roots {
        let start = text[..root.start].rfind('\n').map_or(0, |n| n + 1);
        let mut lines = Vec::new();
        let mut at = start;
        for line in text[start..root.end].split_inclusive('\n') {
            let end = at + line.len();
            let nesting = ranges
                .iter()
                .filter(|(r, _)| r.start < end && at < r.end)
                .map(|(_, depth)| *depth)
                .max()
                .unwrap_or(1);
            let mut pos = line.len() - line.trim_start_matches([' ', '\t']).len();
            let mut count = 0;
            let code_line = code.iter().any(|(r, _)| r.start < end && at < r.end);
            while count < nesting && line.as_bytes().get(pos) == Some(&b'>') {
                count += 1;
                pos += 1;
                if code_line {
                    if matches!(line.as_bytes().get(pos), Some(b' ' | b'\t')) {
                        pos += 1;
                    }
                } else {
                    while matches!(line.as_bytes().get(pos), Some(b' ' | b'\t')) {
                        pos += 1;
                    }
                }
            }
            if count == 0 {
                pos = 0;
            }
            let blank = line[pos..].trim().is_empty();
            lines.push((at, end, pos, nesting, blank));
            at = end;
        }
        let first = lines.iter().position(|line| !line.4);
        let last = lines.iter().rposition(|line| !line.4);
        for (i, (at, end, pos, nesting, blank)) in lines.into_iter().enumerate() {
            if first.is_none() || i < first.unwrap() || i > last.unwrap() {
                let separator = if first.is_some()
                    && i > last.unwrap()
                    && root.end < text.len()
                    && !text[root.end..].starts_with('\n')
                {
                    "\n"
                } else {
                    ""
                };
                edits.push((at..end, separator.into()));
            } else {
                let prefix = format!("{}{}", ">".repeat(nesting), if blank { "" } else { " " });
                if text[at..at + pos] != prefix {
                    edits.push((at..at + pos, prefix));
                }
            }
        }
        for (heading, nesting) in &headings {
            if root.start <= heading.start && heading.end < root.end {
                let next_end = text[heading.end..root.end]
                    .find('\n')
                    .map_or(root.end, |n| heading.end + n);
                let next = text[heading.end..next_end].trim().trim_matches('>').trim();
                if !next.is_empty() {
                    edits.push((
                        heading.end..heading.end,
                        format!("{}\n", ">".repeat(*nesting)),
                    ));
                }
            }
        }
        for (fence, nesting) in &code {
            if root.start > fence.start || fence.end > root.end {
                continue;
            }
            let block = &text[fence.clone()];
            let Some(first) = block.lines().next() else {
                continue;
            };
            let first = first.trim_start_matches(' ');
            let Some(ch @ ('`' | '~')) = first.chars().next() else {
                continue;
            };
            let length = first.chars().take_while(|c| *c == ch).count();
            if length < 3 {
                continue;
            }
            let closed = block.lines().skip(1).last().is_some_and(|line| {
                let line = line.trim_start_matches([' ', '>']);
                let count = line.chars().take_while(|c| *c == ch).count();
                count >= length && line[count..].trim().is_empty()
            });
            if !closed {
                let marker = ch.to_string().repeat(length);
                let newline = if block.ends_with('\n') { "" } else { "\n" };
                edits.push((
                    fence.end..fence.end,
                    format!("{newline}{} {marker}\n", ">".repeat(*nesting)),
                ));
            }
        }
    }
    apply_edits(text, edits)
}

#[cfg(test)]
mod tests {
    use super::{format, format_with_diagnostics, format_with_references, kotlin_space, selected};
    use crate::template::Graph;
    use serde_json::json;
    use std::collections::BTreeMap;
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
    fn renders_markdown_and_resolves_scoped_links() {
        let names = BTreeMap::from([(
            "smoke.Example.member".into(),
            "::smoke::Example::member".into(),
        )]);
        assert_eq!(
            format_with_references(
                "See [member] and [label][member].",
                "smoke.Example",
                &names,
                true
            )
            .unwrap(),
            "See ::smoke::Example::member and [label]::smoke::Example::member."
        );
        assert_eq!(
            format("**bold**\n\n# Heading\n## Next").unwrap(),
            "**bold**\n\n# Heading\n\n## Next"
        );
        assert!(format_with_references("[unknown]", "smoke", &names, true).is_err());
        assert_eq!(
            format_with_references(
                "[external]\n\n[external]: https://example.com",
                "smoke",
                &names,
                true
            )
            .unwrap(),
            "[external]\n\n[external]: https://example.com"
        );
        assert!(kotlin_space('\u{a0}'));
        assert!(kotlin_space('\u{1c}'));
        assert!(!kotlin_space('\u{85}'));
    }
    #[test]
    fn formats_noncanonical_markdown_like_flexmark() {
        assert_eq!(
            format("-  a\n- b\n   -    nested\n\n1.  first\n7. second").unwrap(),
            "- a\n- b\n  - nested\n\n1. first\n2. second"
        );
        assert_eq!(
            format("#head\n\n# header  ##\nunder\n----").unwrap(),
            "#head\n\n# header ##\n\nunder\n-----"
        );
        assert_eq!(
            format("```cpp  extra\n int n;\n```\n\n    indented").unwrap(),
            "```cpp  extra\nint n;\n```\n\n    indented"
        );
        assert_eq!(
            format("a   \nb\\\nc\n\n\n\nlast").unwrap(),
            "a   \nb\\\nc\n\nlast"
        );
        assert_eq!(
            format(">quote\n>    x\n>\n> third").unwrap(),
            "> quote\n> x\n>\n> third"
        );
        assert_eq!(
            format("[ title ]( https://example.com  \" x \" )").unwrap(),
            "[title](https://example.com \" x \")"
        );
        assert_eq!(format("- - foo").unwrap(), "- - foo");
        assert_eq!(format("1. - 2. foo").unwrap(), "1. - 2. foo");
        assert_eq!(format("Foo\n    ***").unwrap(), "Foo\n***");
        assert_eq!(format("foo\n    # bar").unwrap(), "foo\n# bar");
        assert_eq!(
            format("    ```\n    aaa\n    ```").unwrap(),
            "```\naaa\n```\n```"
        );
        assert_eq!(format("> bar\n>\nbaz").unwrap(), "> bar\n\nbaz");
    }

    #[test]
    fn formats_reference_definitions_and_surrounding_blocks() {
        assert_eq!(
            format("[foo]: /url\n\"title\" ok").unwrap(),
            "[foo]: /url\n\n\"title\" ok"
        );
        assert_eq!(
            format("[Foo\n  bar]: /url\n\n[Baz][Foo bar]").unwrap(),
            "[Foo\nbar]: /url\n\n[Baz][Foo bar]"
        );
        assert_eq!(format("aaa\n  \n\n# aaa").unwrap(), "aaa\n\n# aaa");
        assert_eq!(
            format("<table>\n\n  <tr>\n\n</table>").unwrap(),
            "<table>\n\n  <tr>\n\n</table>"
        );
        assert_eq!(
            format("[foo]: /url1\n\n[foo]: /url2\n\n[bar][foo]").unwrap(),
            "[foo]: /url1\n[foo]: /url2\n\n[bar][foo]"
        );
        assert_eq!(
            format("[\n ]\n\n[\n ]: /uri").unwrap(),
            "[\n ]\n\n[\n ]: /uri"
        );
        assert_eq!(
            format("Foo *bar\nbaz*\t\n====").unwrap(),
            "Foo *bar\nbaz*\n===="
        );
    }

    #[test]
    fn formats_html_comments_and_indented_code_blocks() {
        assert_eq!(
            format("<!-- X\n   y\n   z -->\nnext").unwrap(),
            "<!-- X\ny\nz -->\nnext"
        );
        assert_eq!(
            format("<!-- hi -->abcdef\nnext").unwrap(),
            "<!-- hi -->abc-->\nnext"
        );
        assert_eq!(
            format("    chunk1\n      \n      chunk2").unwrap(),
            "chunk1\n\n    chunk2"
        );
    }

    #[test]
    fn retains_nested_code_and_separates_loose_list_items() {
        assert_eq!(
            format("1.  foo\n\n    ```\n    bar\n    ```\n\n    baz").unwrap(),
            "1. foo\n\n   ```\n   bar\n   ```\n\n   baz"
        );
        assert_eq!(format("- a\n- b\n\n- c").unwrap(), "- a\n\n- b\n\n- c");
        assert_eq!(format("- foo\n-\n- bar").unwrap(), "- foo\n- \n- bar");
        assert_eq!(
            format("  1.  A paragraph\n      with two lines.\n\n          indented code\n\n      > A block quote.").unwrap(),
            "1. A paragraph\n   with two lines.\n\n       indented code\n\n   > A block quote."
        );
        assert_eq!(format(" -    one\n\n      two").unwrap(), "- one\n\n  two");
        assert_eq!(format("-\n  foo").unwrap(), "- foo");
        assert_eq!(format("-   \n  foo").unwrap(), "- foo");
        assert_eq!(
            format("- a\n- ```\n  b\n  ```\n- c").unwrap(),
            "- a\n- \n\n  ```\n  b\n  ```\n- c"
        );
        assert_eq!(
            format("1.      indented code\n\n   paragraph\n\n       more code").unwrap(),
            "1. \n\n       indented code\n\n   paragraph\n\n       more code"
        );
        assert_eq!(
            format("- # Foo\n- Bar\n  ---\n  baz").unwrap(),
            "- \n\n  # Foo\n\n- \n\n  Bar\n  ---\n\n  baz"
        );
        assert_eq!(
            format("- a\n  - b\n\n    c\n- d").unwrap(),
            "- a\n  - b\n\n    c\n\n- d"
        );
        assert_eq!(
            format("- a\n  - b\n  - c\n\n- d\n  - e\n  - f").unwrap(),
            "- a\n\n  - b\n  - c\n- d\n\n  - e\n  - f"
        );
        assert_eq!(format("- <div>\n- foo").unwrap(), "- \n\n  <div>\n\n- foo");
    }
    #[test]
    fn unresolved_references_are_returned_as_warnings_or_errors() {
        let names = BTreeMap::new();
        let (rendered, warnings) = format_with_diagnostics(
            "[first] and [second], with [external].\n\n[external]: https://example.com",
            "smoke.Example",
            &names,
            false,
        )
        .unwrap();
        assert!(rendered.contains("[first] and [second]"));
        assert!(warnings.iter().all(|w| w.scope == "smoke.Example"));
        assert_eq!(
            warnings
                .iter()
                .map(|w| w.message.as_str())
                .collect::<Vec<_>>(),
            [
                "Failed to resolve documentation reference [first]",
                "Failed to resolve documentation reference [second]"
            ]
        );
        assert_eq!(
            format_with_diagnostics("[first]", "smoke.Example", &names, true).unwrap_err(),
            warnings[0].message
        );
    }
}
