use std::collections::{BTreeMap, BTreeSet};

#[derive(Clone, Debug)]
pub enum Node {
    Text(String),
    Value(String),
    Partial(String, String),
    Section {
        expression: String,
        inverted: bool,
        body: Vec<Node>,
    },
    Definition(String, Vec<Node>),
}

#[derive(Debug)]
struct Tag {
    start: usize,
    end: usize,
    content: String,
    indent: String,
    suppress_definition_newline: bool,
}

pub fn parse(name: &str, source: &str) -> Result<Vec<Node>, String> {
    if source.len() > 4_000_000 {
        return Err(format!("{name}: template exceeds size limit"));
    }
    let mut tags = Vec::new();
    let mut pos = 0;
    while let Some(relative) = source[pos..].find("{{") {
        let start = pos + relative;
        let triple = source[start..].starts_with("{{{");
        let open = if triple { 3 } else { 2 };
        let close = if triple { "}}}" } else { "}}" };
        let end = source[start + open..]
            .find(close)
            .map(|v| start + open + v + close.len())
            .ok_or_else(|| {
                format!(
                    "{name}:{}: unclosed tag",
                    source[..start].bytes().filter(|x| *x == b'\n').count() + 1
                )
            })?;
        let content = source[start + open..end - close.len()].trim().to_string();
        if content.contains("{{") {
            return Err(format!(
                "{name}:{}: nested tag delimiter",
                source[..start].bytes().filter(|x| *x == b'\n').count() + 1
            ));
        }
        if content.is_empty() {
            return Err(format!("{name}: empty tag"));
        }
        tags.push(Tag {
            start,
            end,
            content,
            indent: String::new(),
            suppress_definition_newline: false,
        });
        pos = end;
    }
    // Tags can span physical lines. Trimou decides standalone status on the
    // text between tags, so newlines inside a comment do not split the line.
    // Track those logical lines without changing the original source offsets.
    let mut line_start = 0;
    let mut first_tag = 0;
    let mut cursor = 0;
    let mut containers: Vec<(String, bool)> = Vec::new();
    let mut definition_depth = 0usize;
    while cursor < source.len() || first_tag < tags.len() {
        let mut next_tag = first_tag;
        let mut end = cursor;
        loop {
            let text_end = tags.get(next_tag).map_or(source.len(), |tag| tag.start);
            if let Some(newline) = source[end..text_end].find('\n') {
                end += newline + 1;
                break;
            }
            if let Some(tag) = tags.get(next_tag) {
                end = tag.end;
                next_tag += 1;
            } else {
                end = source.len();
                break;
            }
        }
        let indices = first_tag..next_tag;
        // A definition disappears before Trimou decides whether the preceding
        // tags are standalone. Its closing newline is then consumed along
        // with those tags if they occupy the rest of the logical line.
        let mut prefix_cursor = line_start;
        let mut prefix_structural = true;
        for i in indices.clone() {
            let tag = &tags[i];
            prefix_structural &= source[prefix_cursor..tag.start]
                .chars()
                .all(|c| c == ' ' || c == '\t' || c == '\r');
            if tag.content.starts_with('+') && i > first_tag && prefix_structural {
                tags[i].suppress_definition_newline = true;
            }
            prefix_structural &= matches!(
                tags[i].content.chars().next(),
                Some('!' | '#' | '^' | '/' | '>')
            );
            prefix_cursor = tags[i].end;
        }
        let mut text_cursor = line_start;
        let standalone = !indices.is_empty()
            && indices.clone().all(|i| {
                let tag = &tags[i];
                let valid = matches!(
                    tag.content.chars().next(),
                    Some('!' | '#' | '^' | '/' | '>' | '+')
                ) && source[text_cursor..tag.start]
                    .chars()
                    .all(|c| c == ' ' || c == '\t' || c == '\r');
                text_cursor = tag.end;
                valid
            })
            && source[text_cursor..end]
                .chars()
                .all(|c| c == ' ' || c == '\t' || c == '\r' || c == '\n');
        // Whitespace inside an inline definition is part of the partial,
        // including indentation next to its boundary tags. A boundary line
        // can also contain body tags, so track containers in lexical order.
        let inside_definition = definition_depth > 0
            || indices
                .clone()
                .any(|i| tags[i].content.starts_with('+') && (i == first_tag || i + 1 < next_tag));
        if standalone && !inside_definition {
            let indent = source[line_start..tags[first_tag].start].to_string();
            if let Some(i) = indices.clone().find(|&i| tags[i].content.starts_with('>')) {
                tags[i].indent = indent;
            }
            tags[first_tag].start = line_start;
            for i in first_tag..next_tag - 1 {
                tags[i].end = tags[i + 1].start;
            }
            if !tags[next_tag - 1].content.starts_with('+') {
                tags[next_tag - 1].end = end;
            }
        }
        for i in indices.clone() {
            let content = &tags[i].content;
            match content.chars().next() {
                Some('#' | '^' | '+') => {
                    if let Some(name) = content[1..].split_whitespace().next() {
                        let definition = content.starts_with('+');
                        definition_depth += usize::from(definition);
                        containers.push((name.to_string(), definition));
                    }
                }
                Some('/')
                    if containers
                        .last()
                        .is_some_and(|(name, _)| name == content[1..].trim()) =>
                {
                    if containers.pop().is_some_and(|(_, definition)| definition) {
                        definition_depth -= 1;
                    }
                }
                _ => {}
            }
        }
        first_tag = next_tag;
        line_start = end;
        cursor = end;
        if end == source.len() {
            break;
        }
    }
    #[allow(clippy::too_many_arguments)]
    fn block(
        name: &str,
        source: &str,
        tags: &[Tag],
        index: &mut usize,
        cursor: &mut usize,
        close: Option<&str>,
        depth: usize,
        definitions: &mut BTreeSet<String>,
    ) -> Result<Vec<Node>, String> {
        if depth > 128 {
            return Err(format!("{name}: nesting limit exceeded"));
        }
        let mut nodes = Vec::new();
        while let Some(tag) = tags.get(*index) {
            if tag.start < *cursor {
                return Err(format!("{name}: overlapping tags"));
            }
            if tag.start > *cursor {
                nodes.push(Node::Text(source[*cursor..tag.start].to_string()));
            }
            *cursor = tag.end;
            *index += 1;
            let c = tag.content.as_str();
            match c.chars().next().unwrap() {
                '!' => {}
                '/' => {
                    let found = c[1..].trim();
                    if Some(found) != close {
                        return Err(format!(
                            "{name}:{}: unexpected closing tag {found}",
                            source[..tag.start].bytes().filter(|x| *x == b'\n').count() + 1
                        ));
                    }
                    return Ok(nodes);
                }
                '#' | '^' | '+' => {
                    let expr = c[1..].trim().to_string();
                    let key = expr
                        .split_whitespace()
                        .next()
                        .ok_or_else(|| format!("{name}: empty section"))?
                        .to_string();
                    if c.starts_with('+') {
                        if expr != key {
                            return Err(format!("{name}: invalid inline partial name {expr}"));
                        }
                        if !definitions.insert(key.clone()) {
                            return Err(format!("{name}: duplicate inline partial {key}"));
                        }
                    } else {
                        let parsed = expression(&expr)?;
                        if c.starts_with('#') {
                            validate_helper(&parsed, true).map_err(|e| format!("{name}: {e}"))?;
                        }
                    }
                    let body = block(
                        name,
                        source,
                        tags,
                        index,
                        cursor,
                        Some(&key),
                        depth + 1,
                        definitions,
                    )?;
                    if c.starts_with('+') {
                        nodes.push(Node::Definition(key, body));
                        let closing = &tags[*index - 1];
                        if tag.suppress_definition_newline
                            && !source[closing.start..closing.end].ends_with('\n')
                        {
                            let rest = &source[*cursor..];
                            let line_len = rest.find('\n').map_or(rest.len(), |i| i + 1);
                            if rest[..line_len]
                                .chars()
                                .all(|c| matches!(c, ' ' | '\t' | '\r' | '\n'))
                            {
                                *cursor += line_len;
                            }
                        }
                        if !tag.suppress_definition_newline
                            && closing.end > closing.start
                            && source[closing.start..closing.end].ends_with('\n')
                        {
                            let ending = if source[closing.start..closing.end].ends_with("\r\n") {
                                "\r\n"
                            } else {
                                "\n"
                            };
                            nodes.push(Node::Text(ending.into()));
                        }
                    } else {
                        nodes.push(Node::Section {
                            expression: expr,
                            inverted: c.starts_with('^'),
                            body,
                        });
                    }
                }
                '>' => nodes.push(Node::Partial(c[1..].trim().to_string(), tag.indent.clone())),
                '&' => {
                    let value = c[1..].trim();
                    validate_helper(&expression(value)?, false)
                        .map_err(|e| format!("{name}: {e}"))?;
                    nodes.push(Node::Value(value.to_string()));
                }
                _ => {
                    validate_helper(&expression(c)?, false).map_err(|e| format!("{name}: {e}"))?;
                    nodes.push(Node::Value(c.to_string()));
                }
            }
        }
        if let Some(c) = close {
            return Err(format!("{name}: unclosed section {c}"));
        }
        if *cursor < source.len() {
            nodes.push(Node::Text(source[*cursor..].to_string()));
            *cursor = source.len();
        }
        Ok(nodes)
    }
    block(
        name,
        source,
        &tags,
        &mut 0,
        &mut 0,
        None,
        0,
        &mut BTreeSet::new(),
    )
}

#[derive(Debug)]
pub struct Expression {
    pub name: String,
    pub args: Vec<String>,
    pub named: BTreeMap<String, String>,
}

// The registration metadata comes from the configured JVM helpers. Inverted
// sections are ordinary lookups in Trimou and do not invoke helpers.
fn validate_helper(e: &Expression, section: bool) -> Result<(), String> {
    let (min, form) = match e.name.as_str() {
        "prefix" | "prefixPartial" | "joinPartial" | "capitalize" | "eval" | "numExpr" => (1, 2),
        "escape" | "resolveName" => (0, 2),
        "join" | "include" => (1, 0),
        "is" => (2, 0),
        "if" | "unless" | "ifPredicate" | "unlessPredicate" | "instanceOf" | "notInstanceOf"
        | "isEq" | "isNotEq" | "case" | "sort" | "filter" | "with" => (1, 1),
        "setJoin" => (3, 1),
        "set" | "each" | "switch" | "default" => (0, 1),
        _ => return Ok(()),
    };
    if (section && form == 0) || (!section && form == 1) {
        return Err(format!("{} does not support this tag form", e.name));
    }
    if e.args.len() < min {
        return Err(format!("{} requires at least {min} argument(s)", e.name));
    }
    if e.name == "set" && e.named.is_empty() {
        return Err("set requires a named argument".into());
    }
    if e.name == "setJoin" && !e.named.contains_key("delimiter") {
        return Err("setJoin requires a delimiter option".into());
    }
    Ok(())
}
pub fn expression(input: &str) -> Result<Expression, String> {
    let mut words = Vec::new();
    let mut word = String::new();
    let mut quote = None;
    for c in input.chars() {
        if let Some(q) = quote {
            word.push(c);
            if c == q {
                quote = None;
            }
            continue;
        }
        if c == '\'' || c == '"' {
            quote = Some(c);
            word.push(c);
        } else if c.is_whitespace() {
            if !word.is_empty() {
                words.push(std::mem::take(&mut word));
            }
        } else {
            word.push(c);
        }
    }
    if quote.is_some() {
        return Err(format!("unterminated quoted argument: {input}"));
    }
    if !word.is_empty() {
        words.push(word);
    }
    let mut it = words.into_iter();
    let name = it.next().ok_or("empty expression")?;
    let mut args = Vec::new();
    let mut named = BTreeMap::new();
    for word in it {
        if let Some((k, v)) = word.split_once('=') {
            if !k.is_empty() && !k.contains(['"', '\'']) {
                if v.is_empty() {
                    return Err(format!("missing value for option {k}"));
                }
                named.insert(k.to_string(), v.to_string());
                continue;
            }
        }
        args.push(word);
    }
    Ok(Expression { name, args, named })
}
