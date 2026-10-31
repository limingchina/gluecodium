use std::collections::BTreeMap;

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
        });
        pos = end;
    }
    // Trimou treats a line containing several structural tags as standalone too.
    let mut line_start = 0;
    let mut first_tag = 0;
    while line_start < source.len() {
        let line_end = source[line_start..]
            .find('\n')
            .map_or(source.len(), |i| line_start + i + 1);
        while first_tag < tags.len() && tags[first_tag].end <= line_start {
            first_tag += 1;
        }
        let mut indices = Vec::new();
        let mut i = first_tag;
        while i < tags.len() && tags[i].start < line_end {
            if tags[i].start >= line_start && tags[i].end <= line_end {
                indices.push(i);
            }
            i += 1;
        }
        if indices.len() > 1
            && indices.iter().all(|i| {
                matches!(
                    tags[*i].content.chars().next(),
                    Some('!' | '#' | '^' | '/' | '>')
                )
            })
        {
            let mut cursor = line_start;
            let mut standalone = true;
            for i in &indices {
                if !source[cursor..tags[*i].start]
                    .chars()
                    .all(|c| c == ' ' || c == '\t' || c == '\r' || c == '\n')
                {
                    standalone = false;
                    break;
                }
                cursor = tags[*i].end;
            }
            if standalone
                && source[cursor..line_end]
                    .chars()
                    .all(|c| c == ' ' || c == '\t' || c == '\r' || c == '\n')
            {
                if tags[indices[0]].start >= line_start {
                    tags[indices[0]].start = line_start;
                }
                let last = *indices.last().unwrap();
                if tags[last].end <= line_end {
                    tags[last].end = line_end;
                }
            }
        }
        line_start = line_end;
    }
    // Standalone structural tags consume their surrounding indentation and newline.
    for tag in &mut tags {
        let c = tag.content.as_str();
        if !matches!(c.chars().next(), Some('!' | '#' | '^' | '/' | '>' | '+')) {
            continue;
        }
        let line_start = source[..tag.start].rfind('\n').map_or(0, |i| i + 1);
        let line_end = source[tag.end..]
            .find('\n')
            .map_or(source.len(), |i| tag.end + i + 1);
        let before = &source[line_start..tag.start];
        let after = &source[tag.end..line_end];
        if before.chars().all(|c| c == ' ' || c == '\t')
            && after
                .chars()
                .all(|c| c == ' ' || c == '\t' || c == '\r' || c == '\n')
        {
            tag.indent = before.to_string();
            tag.start = line_start;
            tag.end = line_end;
        }
    }
    fn block(
        name: &str,
        source: &str,
        tags: &[Tag],
        index: &mut usize,
        cursor: &mut usize,
        close: Option<&str>,
        depth: usize,
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
                    let body = block(name, source, tags, index, cursor, Some(&key), depth + 1)?;
                    if c.starts_with('+') {
                        nodes.push(Node::Definition(key, body));
                        let closing = &tags[*index - 1];
                        if closing.end > closing.start
                            && source[closing.start..closing.end].ends_with('\n')
                        {
                            nodes.push(Node::Text("\n".into()));
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
                '&' => nodes.push(Node::Value(c[1..].trim().to_string())),
                _ => nodes.push(Node::Value(c.to_string())),
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
    block(name, source, &tags, &mut 0, &mut 0, None, 0)
}

#[derive(Debug)]
pub struct Expression {
    pub name: String,
    pub args: Vec<String>,
    pub named: BTreeMap<String, String>,
}
pub fn expression(input: &str) -> Result<Expression, String> {
    let mut words = Vec::new();
    let mut word = String::new();
    let mut quote = None;
    let mut escape = false;
    for c in input.chars() {
        if escape {
            word.push(c);
            escape = false;
            continue;
        }
        if c == '\\' && quote.is_some() {
            word.push(c);
            escape = true;
            continue;
        }
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
            if !k.is_empty() {
                named.insert(k.to_string(), v.to_string());
                continue;
            }
        }
        args.push(word);
    }
    Ok(Expression { name, args, named })
}
