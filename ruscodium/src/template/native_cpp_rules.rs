//! C++ name rules and Java properties decoding.
use std::collections::BTreeMap;
const DEFAULTS: &[(&str, &str)] = &[
    ("field", "lower_snake_case"),
    ("parameter", "lower_snake_case"),
    ("constant", "UPPER_SNAKE_CASE"),
    ("enumerator", "UPPER_SNAKE_CASE"),
    ("method", "lower_snake_case"),
    ("setter", "lower_snake_case"),
    ("setter.prefix", "set"),
    ("getter", "lower_snake_case"),
    ("getter.prefix", "get"),
    ("getter.prefix.boolean", "is"),
    ("type", "UpperCamelCase"),
];
/// Parse a Java .properties file, including continuations and escaped Unicode.
pub fn parse_cpp_properties(input: &str) -> Result<BTreeMap<String, String>, String> {
    let mut lines = Vec::new();
    let mut pending = String::new();
    let mut continued = false;
    for line in input.lines() {
        let line = line.strip_suffix('\r').unwrap_or(line);
        let line = if continued {
            line.trim_start_matches([' ', '\t', '\x0c'])
        } else {
            line
        };
        pending.push_str(line);
        let slashes = pending.chars().rev().take_while(|c| *c == '\\').count();
        continued = slashes % 2 == 1;
        if continued {
            pending.pop();
        } else {
            lines.push(std::mem::take(&mut pending));
        }
    }
    if continued || !pending.is_empty() {
        lines.push(pending);
    }
    let mut result = BTreeMap::new();
    for line in lines {
        let s = line.trim_start_matches([' ', '\t', '\x0c']);
        if s.is_empty() || s.starts_with('#') || s.starts_with('!') {
            continue;
        }
        let mut escaped = false;
        let mut end = s.len();
        for (i, c) in s.char_indices() {
            if !escaped && (c == '=' || c == ':' || matches!(c, ' ' | '\t' | '\x0c')) {
                end = i;
                break;
            }
            if c == '\\' {
                escaped = !escaped;
            } else {
                escaped = false;
            }
        }
        let key = unescape(&s[..end])?;
        let mut value = s[end..].trim_start_matches([' ', '\t', '\x0c']);
        if value.starts_with(['=', ':']) {
            value = &value[1..];
        }
        value = value.trim_start_matches([' ', '\t', '\x0c']);
        result.insert(key, unescape(value)?);
    }
    validate(&result)?;
    Ok(result)
}
fn unescape(input: &str) -> Result<String, String> {
    let mut units = Vec::new();
    let mut chars = input.chars();
    while let Some(c) = chars.next() {
        let c = if c == '\\' {
            match chars.next() {
                Some('t') => '\t',
                Some('n') => '\n',
                Some('r') => '\r',
                Some('f') => '\x0c',
                Some('u') => {
                    let digits: String = chars.by_ref().take(4).collect();
                    if digits.len() != 4 {
                        return Err("invalid properties Unicode escape".into());
                    }
                    units.push(
                        u16::from_str_radix(&digits, 16)
                            .map_err(|_| "invalid properties Unicode escape")?,
                    );
                    continue;
                }
                Some(c) => c,
                None => break,
            }
        } else {
            c
        };
        let mut buf = [0; 2];
        units.extend_from_slice(c.encode_utf16(&mut buf));
    }
    String::from_utf16(&units).map_err(|_| "invalid properties Unicode escape".into())
}
pub fn validate(rules: &BTreeMap<String, String>) -> Result<(), String> {
    for (key, value) in rules {
        if [
            "field",
            "parameter",
            "constant",
            "enumerator",
            "method",
            "type",
            "property",
            "setter",
            "getter",
            "error",
        ]
        .contains(&key.as_str())
            && ![
                "UPPER_SNAKE_CASE",
                "lower_snake_case",
                "UpperCamelCase",
                "lowerCamelCase",
            ]
            .contains(&value.as_str())
        {
            return Err(format!("invalid naming format {value:?} for {key}"));
        }
    }
    Ok(())
}
fn get<'a>(rules: &'a BTreeMap<String, String>, key: &str) -> Option<&'a str> {
    rules
        .get(key)
        .map(String::as_str)
        .or_else(|| DEFAULTS.iter().find(|(k, _)| *k == key).map(|(_, v)| *v))
}
pub fn name(
    rules: &BTreeMap<String, String>,
    key: &str,
    input: &str,
    boolean: bool,
) -> Result<String, String> {
    let format = get(rules, key)
        .ok_or_else(|| format!("native C++ default name rule unsupported for {key}"))?;
    let prefix_key = format!("{key}.prefix");
    let bool_key = format!("{key}.prefix.boolean");
    let suffix_key = format!("{key}.suffix");
    let prefix = if boolean {
        get(rules, &bool_key).or_else(|| get(rules, &prefix_key))
    } else {
        get(rules, &prefix_key)
    };
    let suffix = get(rules, &suffix_key);
    let parts: Vec<&str> = prefix.into_iter().chain([input]).chain(suffix).collect();
    if parts.len() == 1 {
        return apply(format, input);
    }
    match format {
        "lower_snake_case" | "UPPER_SNAKE_CASE" => parts
            .iter()
            .map(|p| apply(format, p))
            .collect::<Result<Vec<_>, _>>()
            .map(|x| x.join("_")),
        "UpperCamelCase" => parts.iter().map(|p| apply(format, p)).collect(),
        "lowerCamelCase" => {
            let mut out = apply(format, parts[0])?;
            for part in &parts[1..] {
                out.push_str(&apply("UpperCamelCase", part)?);
            }
            Ok(out)
        }
        _ => Err(format!("invalid naming format {format}")),
    }
}
fn ascii_lower(c: char) -> char {
    c.to_ascii_lowercase()
}
fn ascii_upper(c: char) -> char {
    c.to_ascii_uppercase()
}
fn capitalize_ascii(s: &str) -> String {
    let mut c = s.chars();
    c.next()
        .map(|f| {
            std::iter::once(ascii_upper(f))
                .chain(c.map(ascii_lower))
                .collect()
        })
        .unwrap_or_default()
}
fn apply(format: &str, input: &str) -> Result<String, String> {
    let mixed = input.chars().any(char::is_lowercase) && input.chars().any(char::is_uppercase);
    match format {
        "lower_snake_case" | "UPPER_SNAKE_CASE" => {
            let mut s = String::new();
            if !input.contains('_') && mixed {
                for (i, c) in input.chars().enumerate() {
                    if c.is_ascii_uppercase() && i > 0 {
                        s.push('_');
                    }
                    s.push(ascii_lower(c));
                }
            } else if input.contains('_') {
                s = input.chars().map(ascii_lower).collect();
            } else {
                s = input.to_lowercase();
            }
            if format == "UPPER_SNAKE_CASE" {
                if input.contains('_') || mixed {
                    s = s.chars().map(ascii_upper).collect();
                } else {
                    s = input.to_uppercase();
                }
            }
            Ok(s)
        }
        "UpperCamelCase" | "lowerCamelCase" => {
            let upper = format == "UpperCamelCase";
            if input.contains('_') {
                let mut parts = input.split('_');
                let first = parts.next().unwrap_or("");
                let mut out = if upper {
                    capitalize_ascii(first)
                } else {
                    first.chars().map(ascii_lower).collect()
                };
                for p in parts {
                    out.push_str(&capitalize_ascii(p));
                }
                Ok(out)
            } else if mixed {
                let mut chars = input.chars();
                Ok(chars
                    .next()
                    .map(|c| {
                        let first = if upper {
                            ascii_upper(c)
                        } else {
                            ascii_lower(c)
                        };
                        first.to_string() + chars.as_str()
                    })
                    .unwrap_or_default())
            } else {
                let s = input.to_lowercase();
                if upper {
                    let mut chars = s.chars();
                    Ok(chars
                        .next()
                        .map(|c| c.to_uppercase().collect::<String>() + chars.as_str())
                        .unwrap_or_default())
                } else {
                    Ok(s)
                }
            }
        }
        _ => Err(format!("invalid naming format {format}")),
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn properties_and_naming_match_jvm_rules() {
        let rules=parse_cpp_properties("method=lowerCamelCase\nfield.prefix=m\ngetter.prefix.boolean=really\nsetter=UPPER_SNAKE_CASE\nsetter.prefix=store\nsetter.suffix=now\ntype=lower_snake_case\n").unwrap();
        assert_eq!(
            name(&rules, "method", "HTTPServer", false).unwrap(),
            "hTTPServer"
        );
        assert_eq!(
            name(&rules, "field", "someField", false).unwrap(),
            "m_some_field"
        );
        assert_eq!(
            name(&rules, "getter", "enabled", true).unwrap(),
            "really_enabled"
        );
        assert_eq!(
            name(&rules, "setter", "someField", false).unwrap(),
            "STORE_SOME_FIELD_NOW"
        );
        assert_eq!(
            name(&rules, "type", "SomeType", false).unwrap(),
            "some_type"
        );
        assert_eq!(name(&rules, "type", "Café", false).unwrap(), "café");
        let escaped =
            parse_cpp_properties("method\\u003dprefix: ignored\nfield.prefix = x\\\n  y\n")
                .unwrap();
        assert_eq!(escaped["field.prefix"], "xy");
        assert_eq!(escaped["method=prefix"], "ignored");
        assert!(parse_cpp_properties("field=not_a_format").is_err());
    }
}
