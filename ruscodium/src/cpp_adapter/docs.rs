//! Bounded parsing of the loader's line-comment documentation syntax.
//!
//! The adapter attaches paths and selects child comments. This module keeps
//! the raw platform sections that the existing generator knows how to render.

use std::collections::BTreeMap;

#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub(super) struct Comment {
    pub sections: Vec<(String, String)>,
    pub is_excluded: bool,
}

#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub(super) struct ParsedDocumentation {
    pub description: Comment,
    pub blocks: BTreeMap<(String, String), Comment>,
}

/// Parse retained lexer tokens, applying the upstream loader's `trimIndent`
/// and per-line trailing whitespace removal before parsing Limedoc.
pub(super) fn parse_documentation(docs: &[String]) -> Result<ParsedDocumentation, String> {
    let mut lines = Vec::new();
    for doc in docs {
        let line = doc
            .strip_prefix("//")
            .ok_or("block documentation comments are unsupported")?;
        if line.contains(['\n', '\r']) {
            return Err("multiline line-comment token is unsupported".into());
        }
        if line.chars().any(|ch| ch.is_control() && ch != '\t') {
            return Err("control character in documentation is unsupported".into());
        }
        lines.push(line);
    }
    while lines.first().is_some_and(|line| line.trim().is_empty()) {
        lines.remove(0);
    }
    while lines.last().is_some_and(|line| line.trim().is_empty()) {
        lines.pop();
    }
    let indent = lines
        .iter()
        .filter(|line| !line.trim().is_empty())
        .map(|line| line.chars().take_while(|c| c.is_whitespace()).count())
        .min()
        .unwrap_or(0);
    let normalized = lines
        .iter()
        .map(|line| {
            let start = line
                .char_indices()
                .nth(indent)
                .map(|(i, _)| i)
                .unwrap_or(line.len());
            line[start..].trim_end()
        })
        .collect::<Vec<_>>()
        .join("\n");
    reject_markdown(&normalized)?;

    let mut result = ParsedDocumentation::default();
    let mut current: Option<(String, String)> = None;
    let mut content = String::new();
    for (index, line) in normalized.split('\n').enumerate() {
        let trimmed = line.trim_start_matches(char::is_whitespace);
        if trimmed.starts_with('@') {
            if let Some(key) = current.take() {
                if content.is_empty() {
                    return Err(
                        "empty documentation block before another block is unsupported".into(),
                    );
                }
                content.push('\n');
                result.blocks.insert(key, parse_comment(&content, false)?);
            } else {
                // The newline separating a description and a tag section is
                // grammar whitespace, not part of the description.
                result.description = parse_comment(content.trim_end_matches('\n'), true)?;
            }
            let (key, initial) = parse_block_header(trimmed)?;
            current = Some(key);
            content.clear();
            content.push_str(initial);
        } else {
            if index != 0 && (!content.is_empty() || current.is_some()) {
                content.push('\n');
            }
            content.push_str(line);
        }
    }
    if let Some(key) = current {
        result.blocks.insert(key, parse_comment(&content, false)?);
    } else {
        result.description = parse_comment(&content, true)?;
    }
    result.description.is_excluded = result.blocks.contains_key(&("exclude".into(), "".into()));
    Ok(result)
}

fn parse_block_header(line: &str) -> Result<((String, String), &str), String> {
    let rest = &line[1..];
    let name_len = rest.bytes().take_while(u8::is_ascii_alphabetic).count();
    if name_len == 0 {
        return Err("invalid documentation block tag".into());
    }
    let name = &rest[..name_len];
    if ![
        "param",
        "return",
        "value",
        "get",
        "set",
        "description",
        "constructor",
        "exclude",
    ]
    .contains(&name)
    {
        return Err(format!("unsupported documentation block tag @{name}"));
    }
    let mut rest = &rest[name_len..];
    let mut parameter = "";
    if let Some(after) = rest.strip_prefix('[') {
        let end = after
            .find(']')
            .ok_or("unterminated documentation block parameter")?;
        parameter = &after[..end];
        let mut chars = parameter.chars();
        if !chars
            .next()
            .is_some_and(|c| c.is_ascii_alphabetic() || c == '_')
            || !chars.all(|c| c.is_ascii_alphanumeric() || c == '_')
        {
            return Err("invalid documentation block parameter".into());
        }
        rest = &after[end + 1..];
    }
    if (name == "param") != !parameter.is_empty() {
        return Err(format!("invalid parameter for documentation block @{name}"));
    }
    if !rest.is_empty() {
        let first = rest.chars().next().unwrap();
        if !first.is_whitespace() {
            return Err("invalid documentation block header".into());
        }
        rest = &rest[first.len_utf8()..];
    }
    Ok(((name.into(), parameter.into()), rest))
}

fn append(sections: &mut Vec<(String, String)>, tag: &str, text: &str) {
    if text.is_empty() {
        return;
    }
    if let Some((last_tag, last_text)) = sections.last_mut() {
        if last_tag == tag && tag.is_empty() {
            last_text.push_str(text);
            return;
        }
    }
    sections.push((tag.into(), text.into()));
}

fn parse_comment(text: &str, description: bool) -> Result<Comment, String> {
    let mut result = Comment::default();
    let mut pos = 0;
    let mut first_word = description;
    let mut line_start = description;
    while pos < text.len() {
        let rest = &text[pos..];
        if rest.starts_with("{@") {
            let (used, tags, value) = parse_inline(rest)?;
            for tag in tags {
                append(&mut result.sections, &tag, &value);
            }
            pos += used;
            line_start = false;
            continue;
        }
        let ch = rest.chars().next().unwrap();
        if ch == '\\' {
            let next = rest[1..]
                .chars()
                .next()
                .ok_or("invalid documentation escape")?;
            if !matches!(next, '@' | '{' | '}' | '\\') {
                return Err("unsupported documentation escape or Markdown".into());
            }
            let n = 1 + next.len_utf8();
            if first_word {
                append(&mut result.sections, "", &rest[..n]);
            } else {
                append(&mut result.sections, "", &rest[1..n]);
            }
            pos += n;
            line_start = false;
            continue;
        }
        if !description && ch == '@' {
            return Err("unescaped @ in documentation block".into());
        }
        if description && line_start && matches!(ch, '@' | '{' | '}') {
            return Err("invalid start of documentation description line".into());
        }
        if ch == '\n' {
            first_word = description;
            line_start = description;
        } else if ch.is_whitespace() {
            if !line_start {
                first_word = false;
            }
        } else {
            line_start = false;
        }
        append(&mut result.sections, "", &rest[..ch.len_utf8()]);
        pos += ch.len_utf8();
    }
    Ok(result)
}

fn parse_inline(text: &str) -> Result<(usize, Vec<String>, String), String> {
    let mut pos = 2;
    let mut tags = Vec::new();
    loop {
        let n = text[pos..]
            .bytes()
            .take_while(u8::is_ascii_alphabetic)
            .count();
        if n == 0 {
            return Err("invalid inline documentation tag".into());
        }
        let tag = &text[pos..pos + n];
        if tag == "Placeholder" {
            return Err("documentation placeholders are unsupported (no placeholder map)".into());
        }
        tags.push(tag.to_string());
        pos += n;
        let separator = text[pos..]
            .chars()
            .next()
            .ok_or("unterminated inline documentation tag")?;
        if !separator.is_whitespace() {
            return Err("invalid inline documentation tag separator".into());
        }
        pos += separator.len_utf8();
        if text[pos..].starts_with('@') {
            pos += 1;
            continue;
        }
        break;
    }
    let mut value = String::new();
    while pos < text.len() {
        let rest = &text[pos..];
        let ch = rest.chars().next().unwrap();
        if ch == '}' {
            return Ok((pos + 1, tags, value));
        }
        if ch == '{' || ch == '@' {
            return Err("invalid nested inline documentation tag".into());
        }
        if ch == '\\' {
            let next = rest[1..]
                .chars()
                .next()
                .ok_or("invalid inline documentation escape")?;
            if !matches!(next, '@' | '{' | '}' | '\\') {
                return Err("unsupported inline escape or Markdown".into());
            }
            value.push(next);
            pos += 1 + next.len_utf8();
        } else {
            value.push(ch);
            pos += ch.len_utf8();
        }
    }
    Err("unterminated inline documentation tag".into())
}

fn reject_markdown(text: &str) -> Result<(), String> {
    for line in text.lines() {
        let s = line.trim_start();
        let ordered_list = s.split_once('.').is_some_and(|(number, tail)| {
            !number.is_empty()
                && number.bytes().all(|b| b.is_ascii_digit())
                && tail.starts_with(' ')
        });
        if s.starts_with("# ")
            || s.starts_with("##")
            || s.starts_with("> ")
            || s.starts_with("- ")
            || s.starts_with("* ")
            || s.starts_with("+ ")
            || s.contains('`')
            || s.matches('*').count() >= 2
            || s.contains("__")
            || s.contains("](")
            || ordered_list
        {
            return Err("structured Markdown documentation is unsupported".into());
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn parse(lines: &[&str]) -> ParsedDocumentation {
        parse_documentation(&lines.iter().map(|s| s.to_string()).collect::<Vec<_>>()).unwrap()
    }

    fn text(comment: &Comment) -> String {
        comment
            .sections
            .iter()
            .filter(|(tag, _)| tag.is_empty())
            .map(|(_, s)| s.as_str())
            .collect()
    }

    #[test]
    fn normalizes_indentation_and_retains_block_content() {
        let doc = parse(&[
            "//    First line.",
            "//      Second line.",
            "//",
            "//    @param[input] Input.",
            "//    continued",
            "//    @return Result.",
        ]);
        assert_eq!(text(&doc.description), "First line.\n  Second line.");
        assert_eq!(
            text(&doc.blocks[&("param".into(), "input".into())]),
            "Input.\ncontinued\n"
        );
        assert_eq!(text(&doc.blocks[&("return".into(), "".into())]), "Result.");
    }

    #[test]
    fn retains_distinct_block_keys_and_last_duplicate() {
        let doc = parse(&[
            "// @param[p0] First",
            "// @param[named] Named",
            "// @param[p0] Last",
            "// @value Value",
            "// @get Get",
            "// @set Set",
            "// @description Description",
            "// @constructor Constructor",
            "// @exclude",
        ]);
        assert_eq!(text(&doc.blocks[&("param".into(), "p0".into())]), "Last\n");
        assert_eq!(
            text(&doc.blocks[&("param".into(), "named".into())]),
            "Named\n"
        );
        assert!(doc.description.is_excluded);
        assert!(!doc.blocks[&("value".into(), "".into())].is_excluded);
    }

    #[test]
    fn preserves_order_platforms_and_escaping() {
        let doc = parse(&["// Before {@Cpp @Java native \\{value\\}} after {@Swift swift}."]);
        assert_eq!(
            doc.description.sections,
            vec![
                ("".into(), "Before ".into()),
                ("Cpp".into(), "native {value}".into()),
                ("Java".into(), "native {value}".into()),
                ("".into(), " after ".into()),
                ("Swift".into(), "swift".into()),
                ("".into(), ".".into())
            ]
        );
    }

    #[test]
    fn rejects_unsupported_and_malformed_forms() {
        for input in [
            "/* block */",
            "// {@Placeholder missing}",
            "// {@Cpp bad",
            "// {@Cpp bad {@Java nested}}",
            "// @param[] bad",
            "// @other text",
            "// **bold**",
            "// [link](url)",
        ] {
            assert!(
                parse_documentation(&[input.into()]).is_err(),
                "accepted {input}"
            );
        }
    }

    #[test]
    fn rejects_control_characters_before_normalization() {
        for control in ['\0', '\u{b}', '\u{c}', '\u{7f}', '\u{85}'] {
            for input in [
                format!("//{control}Text"),
                format!("// Text{control}"),
                format!("// {{@Cpp{control}text}}"),
            ] {
                assert!(
                    parse_documentation(std::slice::from_ref(&input)).is_err(),
                    "accepted {input:?}"
                );
            }
        }
        assert_eq!(text(&parse(&["// A\tword."]).description), "A\tword.");
    }
}
