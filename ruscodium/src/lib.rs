use serde::Serialize;
use std::{
    collections::{BTreeMap, BTreeSet},
    fs,
    path::{Path, PathBuf},
};

#[derive(Debug, Clone, Serialize)]
pub struct Span {
    pub start: usize,
    pub end: usize,
    pub line: usize,
    pub column: usize,
}
#[derive(Debug, Clone, Serialize)]
pub struct Token {
    pub text: String,
    pub span: Span,
    pub kind: String,
}
#[derive(Debug, Clone, Serialize)]
pub struct AnnotationValue {
    pub name: Option<String>,
    pub values: Vec<String>,
}
#[derive(Debug, Clone, Serialize)]
pub struct Annotation {
    pub name: String,
    pub raw: String,
    pub span: Span,
    pub values: Vec<AnnotationValue>,
}
#[derive(Debug, Clone, Serialize)]
pub struct DescriptorValue {
    pub platform: String,
    pub key: String,
    pub value: String,
}
#[derive(Debug, Clone, Serialize)]
pub struct Descriptor {
    pub raw: String,
    pub span: Span,
    pub values: Vec<DescriptorValue>,
}
#[derive(Debug, Clone, Serialize)]
pub struct TypeRef {
    pub name: String,
    pub builtin: bool,
    pub args: Vec<TypeRef>,
    pub nullable: bool,
    pub annotations: Vec<Annotation>,
    pub span: Span,
    pub resolved: Option<String>,
}
#[derive(Debug, Clone, Serialize)]
pub struct Literal {
    pub kind: String,
    pub raw: String,
    pub span: Span,
    pub name: Option<String>,
    pub children: Vec<Literal>,
}
#[derive(Debug, Clone, Serialize)]
pub struct Decl {
    pub kind: String,
    pub name: String,
    pub span: Span,
    pub docs: Vec<String>,
    pub annotations: Vec<Annotation>,
    pub modifiers: Vec<String>,
    pub ty: Option<TypeRef>,
    pub parents: Vec<TypeRef>,
    pub params: Vec<Decl>,
    pub children: Vec<Decl>,
    pub value: Option<String>,
    pub literal: Option<Literal>,
    pub descriptor: Option<Descriptor>,
    pub throws: Option<TypeRef>,
    pub return_docs: Vec<String>,
    pub throws_docs: Vec<String>,
}
#[derive(Debug, Clone, Serialize)]
pub struct File {
    pub path: String,
    pub auxiliary: bool,
    pub package: String,
    pub imports: Vec<String>,
    pub declarations: Vec<Decl>,
}
#[derive(Debug, Clone, Serialize)]
pub struct Model {
    pub schema_version: u32,
    pub files: Vec<File>,
}

fn error(path: &str, span: &Span, message: &str) -> String {
    format!("{}:{}:{}: {}", path, span.line, span.column, message)
}

fn valid_number(s: &str) -> bool {
    fn digits(s: &str) -> bool {
        let b = s.as_bytes();
        !b.is_empty()
            && b[0].is_ascii_digit()
            && b[b.len() - 1].is_ascii_digit()
            && b.iter().all(|c| c.is_ascii_digit() || *c == b'_')
    }
    for suffix in ["min", "ms", "us", "ns", "d", "h", "s"] {
        if let Some(n) = s.strip_suffix(suffix) {
            return !n.contains('_') && digits(n) && (n.len() == 1 || !n.starts_with('0'));
        }
    }
    let (mantissa, exp) = match s.find(['e', 'E']) {
        Some(i) => (&s[..i], Some(&s[i + 1..])),
        None => (s, None),
    };
    if let Some(e) = exp {
        let e = e.strip_prefix(['+', '-']).unwrap_or(e);
        if !digits(e) {
            return false;
        }
    }
    if let Some((a, b)) = mantissa.split_once('.') {
        return (a.is_empty() || digits(a)) && digits(b);
    }
    digits(mantissa) && (exp.is_some() || mantissa.len() == 1 || !mantissa.starts_with('0'))
}

pub fn lex(path: &str, src: &str) -> Result<Vec<Token>, String> {
    let mut out = Vec::new();
    let mut i = 0;
    let mut line = 1;
    let mut col = 1;
    let mut previous_cr = false;
    while i < src.len() {
        let start = i;
        let sl = line;
        let sc = col;
        let tail = &src[i..];
        let c = tail.chars().next().unwrap();
        let (n, kind) = if c.is_whitespace() {
            (c.len_utf8(), "space")
        } else if c == '#' {
            (tail.find(['\n', '\r']).unwrap_or(tail.len()), "space")
        } else if tail.starts_with("//") {
            (tail.find(['\n', '\r']).unwrap_or(tail.len()), "doc")
        } else if tail.starts_with("/*") {
            match tail.find("*/") {
                Some(n) => (n + 2, "doc"),
                None => {
                    return Err(error(
                        path,
                        &Span {
                            start,
                            end: src.len(),
                            line: sl,
                            column: sc,
                        },
                        "unterminated comment",
                    ))
                }
            }
        } else if let Some(rest) = tail.strip_prefix("\"\"\"") {
            match rest.find("\"\"\"") {
                Some(n) => (n + 6, "string"),
                None => {
                    return Err(error(
                        path,
                        &Span {
                            start,
                            end: src.len(),
                            line: sl,
                            column: sc,
                        },
                        "unterminated multiline string",
                    ))
                }
            }
        } else if c == '"' {
            let mut n = 1;
            let mut done = false;
            let b = tail.as_bytes();
            while n < b.len() {
                if b[n] == b'"' {
                    n += 1;
                    done = true;
                    break;
                }
                if b[n] == b'\\' {
                    n += 1;
                    if n >= b.len() || !b"tbrn\"\\".contains(&b[n]) {
                        return Err(error(
                            path,
                            &Span {
                                start,
                                end: start + n,
                                line: sl,
                                column: sc,
                            },
                            "invalid string escape",
                        ));
                    }
                }
                if b[n] == b'\n' || b[n] == b'\r' {
                    break;
                }
                n += 1;
            }
            if !done {
                return Err(error(
                    path,
                    &Span {
                        start,
                        end: start + n,
                        line: sl,
                        column: sc,
                    },
                    "unterminated string",
                ));
            }
            (n, "string")
        } else if c == '`' {
            match tail[1..].find('`') {
                Some(n) if n > 0 && !tail[1..1 + n].contains(['\n', '\r']) => (n + 2, "id"),
                _ => {
                    return Err(error(
                        path,
                        &Span {
                            start,
                            end: start + 1,
                            line: sl,
                            column: sc,
                        },
                        "unterminated quoted identifier",
                    ))
                }
            }
        } else if c.is_ascii_alphabetic() || c == '_' {
            (
                tail.find(|x: char| !x.is_ascii_alphanumeric() && x != '_')
                    .unwrap_or(tail.len()),
                "id",
            )
        } else if c.is_ascii_digit()
            || (c == '.' && tail.as_bytes().get(1).is_some_and(u8::is_ascii_digit))
        {
            let bytes = tail.as_bytes();
            let mut n = 1;
            while n < bytes.len()
                && (bytes[n].is_ascii_alphanumeric()
                    || bytes[n] == b'_'
                    || bytes[n] == b'.'
                    || ((bytes[n] == b'+' || bytes[n] == b'-')
                        && (bytes[n - 1] == b'e' || bytes[n - 1] == b'E')))
            {
                n += 1
            }
            let raw = &tail[..n];
            if !valid_number(raw) {
                return Err(error(
                    path,
                    &Span {
                        start,
                        end: start + n,
                        line: sl,
                        column: sc,
                    },
                    "invalid numeric literal",
                ));
            }
            (n, "number")
        } else if tail.starts_with("->") {
            (2, "punct")
        } else if "=@:,.+-?(){}<>[]".contains(c) {
            (1, "punct")
        } else {
            return Err(error(
                path,
                &Span {
                    start,
                    end: start + c.len_utf8(),
                    line: sl,
                    column: sc,
                },
                &format!("unexpected character {c:?}"),
            ));
        };
        let text = &src[i..i + n];
        for ch in text.chars() {
            if ch == '\r' {
                line += 1;
                col = 1;
            } else if ch == '\n' {
                if !previous_cr {
                    line += 1;
                }
                col = 1;
            } else {
                col += 1;
            }
            previous_cr = ch == '\r';
        }
        i += n;
        if kind != "space" {
            out.push(Token {
                text: text.to_string(),
                span: Span {
                    start,
                    end: i,
                    line: sl,
                    column: sc,
                },
                kind: kind.to_string(),
            })
        }
    }
    out.push(Token {
        text: "<eof>".into(),
        span: Span {
            start: i,
            end: i,
            line,
            column: col,
        },
        kind: "eof".into(),
    });
    Ok(out)
}

struct Parser<'a> {
    path: &'a str,
    src: &'a str,
    t: Vec<Token>,
    i: usize,
}
impl<'a> Parser<'a> {
    fn peek(&self) -> &str {
        &self.t[self.i].text
    }
    fn span(&self) -> Span {
        self.t[self.i].span.clone()
    }
    fn next(&mut self) -> String {
        let s = self.peek().to_string();
        if self.i + 1 < self.t.len() {
            self.i += 1
        }
        s
    }
    fn eat(&mut self, s: &str) -> bool {
        if self.peek() == s {
            self.next();
            true
        } else {
            false
        }
    }
    fn expect(&mut self, s: &str) -> Result<(), String> {
        if self.eat(s) {
            Ok(())
        } else {
            Err(error(
                self.path,
                &self.span(),
                &format!("expected {s}, found {}", self.peek()),
            ))
        }
    }
    fn id(&mut self) -> Result<String, String> {
        const RESERVED: &[&str] = &[
            "class",
            "const",
            "constructor",
            "field",
            "fun",
            "enum",
            "exception",
            "external",
            "get",
            "import",
            "interface",
            "lambda",
            "narrow",
            "open",
            "package",
            "property",
            "set",
            "static",
            "struct",
            "throws",
            "typealias",
            "Void",
            "Boolean",
            "Float",
            "Double",
            "Byte",
            "Short",
            "Int",
            "Long",
            "UByte",
            "UShort",
            "UInt",
            "ULong",
            "String",
            "Blob",
            "Date",
            "Duration",
            "Locale",
            "List",
            "Map",
            "Set",
            "true",
            "false",
            "null",
            "NaN",
            "Infinity",
        ];
        if self.t[self.i].kind == "id" && !RESERVED.contains(&self.peek()) {
            let text = self.next();
            if text.starts_with('`') && text.contains('.') {
                return Err(error(
                    self.path,
                    &self.t[self.i - 1].span,
                    "quoted identifiers containing dots are not yet supported",
                ));
            }
            Ok(text.trim_matches('`').to_string())
        } else {
            Err(error(self.path, &self.span(), "expected identifier"))
        }
    }
    fn qualified(&mut self) -> Result<String, String> {
        let mut s = self.id()?;
        while self.eat(".") {
            s.push('.');
            s.push_str(&self.id()?)
        }
        Ok(s)
    }
    fn meta(&mut self) -> Result<(Vec<String>, Vec<Annotation>), String> {
        let mut docs = Vec::new();
        let mut attrs = Vec::new();
        loop {
            if self.t[self.i].kind == "doc" {
                docs.push(self.next())
            } else if self.eat("@") {
                let mut span = self.t[self.i - 1].span.clone();
                let name = self.id()?;
                let mut values = Vec::new();
                if self.eat("(") {
                    loop {
                        let mut value = AnnotationValue {
                            name: None,
                            values: Vec::new(),
                        };
                        if self.t[self.i].kind == "string" {
                            value.values.push(self.next())
                        } else {
                            value.name = Some(self.id()?);
                            if self.eat("=") {
                                if self.eat("[") {
                                    loop {
                                        self.string()?;
                                        value.values.push(self.t[self.i - 1].text.clone());
                                        if !self.eat(",") {
                                            break;
                                        }
                                    }
                                    self.expect("]")?;
                                } else {
                                    self.string()?;
                                    value.values.push(self.t[self.i - 1].text.clone());
                                }
                            }
                        }
                        values.push(value);
                        if !self.eat(",") {
                            break;
                        }
                    }
                    self.expect(")")?;
                }
                span.end = self.t[self.i - 1].span.end;
                attrs.push(Annotation {
                    name,
                    raw: self.src[span.start..span.end].into(),
                    span,
                    values,
                });
            } else {
                break;
            }
        }
        Ok((docs, attrs))
    }
    fn string(&mut self) -> Result<(), String> {
        if self.t[self.i].kind != "string" || self.peek().starts_with("\"\"\"") {
            return Err(error(
                self.path,
                &self.span(),
                "expected single-line string",
            ));
        }
        self.next();
        Ok(())
    }
    fn newline(&self) -> Result<(), String> {
        let previous = &self.t[self.i - 1];
        if self.peek() == "<eof>"
            || self.src[previous.span.end..self.span().start].contains(['\n', '\r'])
        {
            Ok(())
        } else {
            Err(error(self.path, &self.span(), "expected newline"))
        }
    }
    fn typ(&mut self) -> Result<TypeRef, String> {
        let (_, annotations) = self.meta()?;
        let span = self.span();
        let builtin = BUILTINS.contains(&self.peek());
        let name = if builtin {
            self.next()
        } else {
            self.qualified()?
        };
        let mut args = Vec::new();
        if self.eat("<") {
            loop {
                args.push(self.typ()?);
                if !self.eat(",") {
                    break;
                }
            }
            self.expect(">")?;
        }
        let nullable = self.eat("?");
        Ok(TypeRef {
            name,
            builtin,
            args,
            nullable,
            annotations,
            span,
            resolved: None,
        })
    }
    fn decl(&mut self, context: &str) -> Result<Decl, String> {
        let (docs, annotations) = self.meta()?;
        let span = self.span();
        let mut modifiers = Vec::new();
        while ["open", "narrow", "static"].contains(&self.peek()) {
            modifiers.push(self.next())
        }
        let kind = match self.peek() {
            "class" | "interface" | "struct" | "enum" | "const" | "typealias" | "exception"
            | "lambda" | "fun" | "constructor" | "property" => self.next(),
            "field" => {
                self.next();
                self.expect("constructor")?;
                "field_constructor".into()
            }
            _ if context == "struct" => "field".into(),
            _ if context == "enum" => "enumerator".into(),
            _ => {
                return Err(error(
                    self.path,
                    &span,
                    &format!("expected declaration, found {}", self.peek()),
                ))
            }
        };
        let allowed = match context {
            "file" => matches!(
                kind.as_str(),
                "class" | "interface" | "struct" | "enum" | "typealias" | "exception" | "lambda"
            ),
            "class" | "interface" => matches!(
                kind.as_str(),
                "class"
                    | "interface"
                    | "struct"
                    | "enum"
                    | "typealias"
                    | "exception"
                    | "lambda"
                    | "const"
                    | "fun"
                    | "constructor"
                    | "property"
            ),
            "struct" => kind != "property" && kind != "enumerator",
            "enum" => kind == "enumerator",
            _ => false,
        };
        if !allowed {
            return Err(error(
                self.path,
                &span,
                &format!("{kind} is not allowed in {context}"),
            ));
        }
        if modifiers.iter().any(|m| match m.as_str() {
            "open" => kind != "class",
            "narrow" => kind != "interface",
            "static" => kind != "fun" && kind != "property",
            _ => true,
        }) || modifiers.len() > 1
        {
            return Err(error(self.path, &span, "invalid declaration modifier"));
        }
        let name = if kind == "field_constructor" {
            "constructor".into()
        } else {
            self.id()?
        };
        let mut d = Decl {
            kind: kind.clone(),
            name,
            span,
            docs,
            annotations,
            modifiers,
            ty: None,
            parents: Vec::new(),
            params: Vec::new(),
            children: Vec::new(),
            value: None,
            literal: None,
            descriptor: None,
            throws: None,
            return_docs: Vec::new(),
            throws_docs: Vec::new(),
        };
        match kind.as_str() {
            "class" | "interface" | "struct" | "enum" => {
                if self.eat(":") {
                    if kind != "class" && kind != "interface" {
                        return Err(error(
                            self.path,
                            &self.span(),
                            "only classes and interfaces can inherit",
                        ));
                    }
                    loop {
                        d.parents.push(self.typ()?);
                        if !self.eat(",") {
                            break;
                        }
                    }
                }
                self.expect("{")?;
                if self.peek() == "external" {
                    d.descriptor = Some(self.descriptor()?)
                }
                while self.peek() != "}" {
                    if self.peek() == "<eof>" {
                        return Err(error(self.path, &self.span(), "expected }"));
                    }
                    d.children.push(self.decl(&kind)?);
                    if kind == "enum" && !self.eat(",") {
                        break;
                    }
                }
                self.expect("}")?;
                if (kind == "struct" || kind == "enum") && d.children.is_empty() {
                    return Err(error(self.path, &d.span, "empty struct or enum"));
                }
            }
            "fun" | "constructor" | "field_constructor" => {
                self.expect("(")?;
                while self.peek() != ")" {
                    let (docs, annotations) = self.meta()?;
                    let span = self.span();
                    let name = self.id()?;
                    let ty = if kind != "field_constructor" {
                        self.expect(":")?;
                        Some(self.typ()?)
                    } else {
                        None
                    };
                    d.params.push(Decl {
                        kind: "parameter".into(),
                        name,
                        span,
                        docs,
                        annotations,
                        modifiers: vec![],
                        ty,
                        parents: vec![],
                        params: vec![],
                        children: vec![],
                        value: None,
                        literal: None,
                        descriptor: None,
                        throws: None,
                        return_docs: Vec::new(),
                        throws_docs: Vec::new(),
                    });
                    if !self.eat(",") {
                        break;
                    }
                }
                self.expect(")")?;
                if kind == "fun" && self.eat(":") {
                    let (docs, attrs) = self.meta()?;
                    d.return_docs = docs;
                    let mut ty = self.typ()?;
                    ty.annotations.splice(0..0, attrs);
                    d.ty = Some(ty)
                }
                if kind != "field_constructor" && self.eat("throws") {
                    let (docs, attrs) = self.meta()?;
                    d.throws_docs = docs;
                    let mut ty = self.typ()?;
                    ty.annotations.splice(0..0, attrs);
                    d.throws = Some(ty)
                }
            }
            "property" | "field" | "const" => {
                self.expect(":")?;
                d.ty = Some(self.typ()?);
                if kind == "const" {
                    self.expect("=")?;
                    let literal = self.literal()?;
                    d.value = Some(literal.raw.clone());
                    d.literal = Some(literal);
                } else if kind == "field" && self.eat("=") {
                    let literal = self.literal()?;
                    d.value = Some(literal.raw.clone());
                    d.literal = Some(literal)
                }
                if kind == "field" && self.peek() == "external" {
                    d.descriptor = Some(self.descriptor()?)
                }
                if kind == "property" && self.eat("{") {
                    while self.peek() != "}" {
                        let (docs, annotations) = self.meta()?;
                        let span = self.span();
                        let name = self.next();
                        if (d.children.is_empty() && name != "get")
                            || (d.children.len() == 1 && name != "set")
                            || d.children.len() > 1
                        {
                            return Err(error(self.path, &span, "expected get or set"));
                        }
                        let descriptor = if self.peek() == "external" {
                            Some(self.descriptor()?)
                        } else {
                            None
                        };
                        d.children.push(Decl {
                            kind: "accessor".into(),
                            name,
                            span,
                            docs,
                            annotations,
                            modifiers: vec![],
                            ty: None,
                            parents: vec![],
                            params: vec![],
                            children: vec![],
                            value: None,
                            literal: None,
                            descriptor,
                            throws: None,
                            return_docs: Vec::new(),
                            throws_docs: Vec::new(),
                        })
                    }
                    if d.children.is_empty() {
                        return Err(error(self.path, &self.span(), "expected getter"));
                    }
                    self.expect("}")?;
                }
            }
            "enumerator" => {
                if self.eat("=") {
                    let literal = self.literal()?;
                    d.value = Some(literal.raw.clone());
                    d.literal = Some(literal)
                }
            }
            "typealias" => {
                self.expect("=")?;
                d.ty = Some(self.typ()?)
            }
            "exception" => {
                self.expect("(")?;
                d.ty = Some(self.typ()?);
                self.expect(")")?
            }
            "lambda" => {
                self.expect("=")?;
                self.expect("(")?;
                while self.peek() != ")" {
                    let span = self.span();
                    let name = if self.t.get(self.i + 1).is_some_and(|t| t.text == ":") {
                        let n = self.id()?;
                        self.expect(":")?;
                        n
                    } else {
                        String::new()
                    };
                    let ty = Some(self.typ()?);
                    d.params.push(Decl {
                        kind: "parameter".into(),
                        name,
                        span,
                        docs: vec![],
                        annotations: vec![],
                        modifiers: vec![],
                        ty,
                        parents: vec![],
                        params: vec![],
                        children: vec![],
                        value: None,
                        literal: None,
                        descriptor: None,
                        throws: None,
                        return_docs: Vec::new(),
                        throws_docs: Vec::new(),
                    });
                    if !self.eat(",") {
                        break;
                    }
                }
                self.expect(")")?;
                self.expect("->")?;
                d.ty = Some(self.typ()?)
            }
            _ => {}
        }
        if matches!(
            kind.as_str(),
            "class"
                | "interface"
                | "struct"
                | "enum"
                | "const"
                | "typealias"
                | "exception"
                | "lambda"
                | "property"
        ) {
            self.newline()?;
        }
        Ok(d)
    }
    fn descriptor(&mut self) -> Result<Descriptor, String> {
        let mut span = self.span();
        self.expect("external")?;
        self.expect("{")?;
        let mut values = Vec::new();
        while self.peek() != "}" {
            let platform = self.id()?;
            let key = self.id()?;
            self.string()?;
            let value = self.t[self.i - 1].text.clone();
            values.push(DescriptorValue {
                platform,
                key,
                value,
            });
        }
        if values.is_empty() {
            return Err(error(
                self.path,
                &self.span(),
                "expected external descriptor value",
            ));
        }
        self.expect("}")?;
        span.end = self.t[self.i - 1].span.end;
        Ok(Descriptor {
            raw: self.src[span.start..span.end].into(),
            span,
            values,
        })
    }
    fn literal(&mut self) -> Result<Literal, String> {
        let span = self.span();
        let start = span.start;
        let mut children = Vec::new();
        let kind = if self.eat("{") {
            if self.peek() != "}" {
                loop {
                    let name = if self.t.get(self.i + 1).is_some_and(|t| t.text == "=") {
                        let n = self.id()?;
                        self.expect("=")?;
                        Some(n)
                    } else {
                        None
                    };
                    let mut item = self.literal()?;
                    item.name = name;
                    children.push(item);
                    if !self.eat(",") {
                        break;
                    }
                }
            }
            self.expect("}")?;
            "struct"
        } else if self.eat("[") {
            let mut map = None;
            if self.peek() != "]" {
                loop {
                    let key = self.literal()?;
                    let is_map = self.eat(":");
                    if map.is_some_and(|m| m != is_map) {
                        return Err(error(
                            self.path,
                            &self.span(),
                            "cannot mix map and list entries",
                        ));
                    }
                    map = Some(is_map);
                    children.push(key);
                    if is_map {
                        children.push(self.literal()?);
                    }
                    if !self.eat(",") {
                        break;
                    }
                }
            }
            self.expect("]")?;
            if map == Some(true) {
                "map"
            } else {
                "list"
            }
        } else {
            let signed = self.eat("+") || self.eat("-");
            let token = self.t[self.i].clone();
            if !["id", "number", "string"].contains(&token.kind.as_str()) {
                return Err(error(self.path, &self.span(), "expected literal"));
            }
            if signed && token.kind != "number" && token.text != "Infinity" {
                return Err(error(self.path, &self.span(), "expected numeric literal"));
            }
            if token.kind == "id"
                && !["true", "false", "null", "NaN", "Infinity"].contains(&token.text.as_str())
            {
                self.id()?;
            } else {
                self.next();
            }
            while self.eat(".") {
                self.id()?;
            }
            let positional = if self.eat("(") {
                if self.t[self.i].kind != "number"
                    || !self.peek().chars().all(|c| c.is_ascii_digit() || c == '_')
                {
                    return Err(error(self.path, &self.span(), "expected integer"));
                }
                self.next();
                self.expect(")")?;
                true
            } else {
                false
            };
            if positional {
                "positional_enumerator"
            } else if token.kind == "string" {
                "string"
            } else if token.kind == "number" {
                "number"
            } else if token.text == "true" || token.text == "false" {
                "boolean"
            } else if token.text == "null" {
                "null"
            } else if token.text == "NaN" || token.text == "Infinity" {
                "number"
            } else {
                "reference"
            }
        };
        let mut span = span;
        span.end = self.t[self.i - 1].span.end;
        Ok(Literal {
            kind: kind.into(),
            raw: self.src[start..span.end].into(),
            span,
            name: None,
            children,
        })
    }
}
pub fn parse(path: &str, src: &str, auxiliary: bool) -> Result<File, String> {
    let t = lex(path, src)?;
    let mut p = Parser { path, src, t, i: 0 };
    p.expect("package")?;
    let package = p.qualified()?;
    p.newline()?;
    let mut imports = Vec::new();
    while p.eat("import") {
        imports.push(p.qualified()?);
        p.newline()?
    }
    let mut declarations = Vec::new();
    while p.peek() != "<eof>" {
        declarations.push(p.decl("file")?)
    }
    if declarations.is_empty() {
        return Err(error(path, &p.span(), "expected declaration"));
    }
    Ok(File {
        path: path.into(),
        auxiliary,
        package,
        imports,
        declarations,
    })
}

pub fn collect(paths: &[PathBuf]) -> Result<Vec<PathBuf>, String> {
    fn walk(
        p: &Path,
        out: &mut BTreeSet<PathBuf>,
        visited: &mut BTreeSet<PathBuf>,
    ) -> Result<(), String> {
        if p.is_dir() {
            let canonical = fs::canonicalize(p).map_err(|e| format!("{}: {e}", p.display()))?;
            if !visited.insert(canonical) {
                return Ok(());
            }
            let entries = fs::read_dir(p).map_err(|e| format!("{}: {e}", p.display()))?;
            for entry in entries {
                walk(&entry.map_err(|e| e.to_string())?.path(), out, visited)?
            }
        } else if p.is_file() {
            if p.extension().is_some_and(|e| e == "lime") {
                out.insert(fs::canonicalize(p).map_err(|e| e.to_string())?);
            }
        } else {
            return Err(format!("{}: input does not exist", p.display()));
        }
        Ok(())
    }
    let mut out = BTreeSet::new();
    let mut visited = BTreeSet::new();
    for p in paths {
        walk(p, &mut out, &mut visited)?
    }
    Ok(out.into_iter().collect())
}
pub fn load(inputs: &[PathBuf], aux: &[PathBuf]) -> Result<Model, String> {
    let main = collect(inputs)?;
    let aux = collect(aux)?;
    let mainset: BTreeSet<_> = main.iter().cloned().collect();
    let mut files = Vec::new();
    for path in main
        .iter()
        .chain(aux.iter().filter(|p| !mainset.contains(*p)))
    {
        let src = fs::read_to_string(path).map_err(|e| format!("{}: {e}", path.display()))?;
        files.push(parse(
            &path.display().to_string(),
            &src,
            !mainset.contains(path),
        )?)
    }
    Ok(Model {
        schema_version: 1,
        files,
    })
}

const BUILTINS: &[&str] = &[
    "Byte", "Short", "Int", "Long", "UByte", "UShort", "UInt", "ULong", "Boolean", "String",
    "Float", "Double", "Blob", "Date", "Duration", "Locale", "Void", "List", "Map", "Set",
];
pub fn resolve(model: &mut Model) -> Result<(), String> {
    fn index(
        ds: &[Decl],
        prefix: &str,
        map: &mut BTreeMap<String, String>,
        path: &str,
    ) -> Result<(), String> {
        for d in ds {
            if [
                "class",
                "interface",
                "struct",
                "enum",
                "typealias",
                "exception",
                "lambda",
            ]
            .contains(&d.kind.as_str())
            {
                let name = format!("{prefix}.{}", d.name);
                if map.insert(name.clone(), d.kind.clone()).is_some() {
                    return Err(error(
                        path,
                        &d.span,
                        &format!("duplicate declaration {name}"),
                    ));
                }
                index(&d.children, &name, map, path)?
            }
        }
        Ok(())
    }
    let mut symbols = BTreeMap::new();
    for f in &model.files {
        index(&f.declarations, &f.package, &mut symbols, &f.path)?
    }
    fn find(
        name: &str,
        scope: &str,
        imports: &[String],
        symbols: &BTreeMap<String, String>,
    ) -> Vec<String> {
        let mut candidates = BTreeSet::new();
        for import in imports {
            let short = import.rsplit('.').next().unwrap_or(import);
            if name == short || name.starts_with(&format!("{short}.")) {
                let full = format!("{}{}", import, &name[short.len()..]);
                if symbols.contains_key(&full) {
                    candidates.insert(full);
                }
            }
        }
        let mut current = scope;
        loop {
            let full = if current.is_empty() {
                name.to_string()
            } else {
                format!("{current}.{name}")
            };
            if symbols.contains_key(&full) {
                candidates.insert(full);
            }
            match current.rsplit_once('.') {
                Some((p, _)) => current = p,
                None if !current.is_empty() => current = "",
                None => break,
            }
        }
        candidates.into_iter().collect()
    }
    fn ty(
        t: &mut TypeRef,
        scope: &str,
        imports: &[String],
        symbols: &BTreeMap<String, String>,
        path: &str,
    ) -> Result<(), String> {
        for a in &mut t.args {
            ty(a, scope, imports, symbols, path)?
        }
        if t.builtin {
            let arity = match t.name.as_str() {
                "List" | "Set" => 1,
                "Map" => 2,
                _ => 0,
            };
            if t.args.len() != arity {
                return Err(error(
                    path,
                    &t.span,
                    &format!("{} expects {arity} type arguments", t.name),
                ));
            }
            return Ok(());
        }
        if !t.args.is_empty() {
            return Err(error(
                path,
                &t.span,
                "user-defined types do not accept type arguments",
            ));
        }
        let candidates = find(&t.name, scope, imports, symbols);
        match candidates.len() {
            0 => Err(error(path, &t.span, &format!("unresolved type {}", t.name))),
            1 => {
                t.resolved = Some(candidates[0].clone());
                Ok(())
            }
            _ => Err(error(
                path,
                &t.span,
                &format!("ambiguous type {}: {}", t.name, candidates.join(", ")),
            )),
        }
    }
    fn visit(
        ds: &mut [Decl],
        scope: &str,
        imports: &[String],
        symbols: &BTreeMap<String, String>,
        path: &str,
    ) -> Result<(), String> {
        let mut members = BTreeSet::new();
        for d in ds {
            if !matches!(
                d.kind.as_str(),
                "fun" | "constructor" | "field_constructor" | "parameter"
            ) && !members.insert(d.name.clone())
            {
                return Err(error(
                    path,
                    &d.span,
                    &format!("duplicate member {}", d.name),
                ));
            }
            let inner = if matches!(d.kind.as_str(), "class" | "interface" | "struct" | "enum") {
                format!("{scope}.{}", d.name)
            } else {
                scope.to_string()
            };
            if let Some(t) = &mut d.ty {
                ty(t, &inner, imports, symbols, path)?;
                if t.resolved
                    .as_ref()
                    .and_then(|n| symbols.get(n))
                    .is_some_and(|k| k == "exception")
                    && d.kind != "exception"
                {
                    return Err(error(
                        path,
                        &t.span,
                        "exception cannot be used as a value type",
                    ));
                }
                if t.builtin
                    && ((t.name == "Void" && d.kind != "fun" && d.kind != "lambda")
                        || (t.name == "Void" && t.nullable))
                {
                    return Err(error(path, &t.span, "Void is not valid here"));
                }
            }
            for t in &mut d.parents {
                ty(t, scope, imports, symbols, path)?;
                let kind = t.resolved.as_ref().and_then(|n| symbols.get(n));
                if !matches!(
                    kind.map(String::as_str),
                    Some("class" | "interface" | "typealias")
                ) || (d.kind == "interface"
                    && !matches!(kind.map(String::as_str), Some("interface" | "typealias")))
                {
                    return Err(error(path, &t.span, "invalid inheritance target"));
                }
            }
            if d.kind == "struct" {
                let fields: BTreeSet<_> = d
                    .children
                    .iter()
                    .filter(|c| c.kind == "field")
                    .map(|c| c.name.as_str())
                    .collect();
                for c in &d.children {
                    if c.kind == "field_constructor" {
                        for p in &c.params {
                            if !fields.contains(p.name.as_str()) {
                                return Err(error(
                                    path,
                                    &p.span,
                                    "field constructor references unknown field",
                                ));
                            }
                        }
                    }
                }
            }
            if let Some(t) = &mut d.throws {
                ty(t, scope, imports, symbols, path)?;
                if t.resolved
                    .as_ref()
                    .and_then(|n| symbols.get(n))
                    .map(String::as_str)
                    != Some("exception")
                {
                    return Err(error(path, &t.span, "throws requires an exception"));
                }
            }
            let mut params = BTreeSet::new();
            for p in &d.params {
                if !p.name.is_empty() && !params.insert(p.name.clone()) {
                    return Err(error(
                        path,
                        &p.span,
                        &format!("duplicate parameter {}", p.name),
                    ));
                }
            }
            visit(&mut d.params, &inner, imports, symbols, path)?;
            visit(&mut d.children, &inner, imports, symbols, path)?;
        }
        Ok(())
    }
    for f in &mut model.files {
        for i in &f.imports {
            if !symbols.contains_key(i) {
                return Err(format!("{}: unresolved import {i}", f.path));
            }
        }
        visit(
            &mut f.declarations,
            &f.package,
            &f.imports,
            &symbols,
            &f.path,
        )?
    }
    fn edges(ds: &[Decl], scope: &str, graph: &mut BTreeMap<String, Vec<String>>) {
        fn type_edges(t: &TypeRef, out: &mut Vec<String>) {
            if let Some(r) = &t.resolved {
                out.push(r.clone())
            }
            for a in &t.args {
                type_edges(a, out)
            }
        }
        for d in ds {
            let full = format!("{scope}.{}", d.name);
            if d.kind == "typealias" {
                if let Some(t) = &d.ty {
                    type_edges(t, graph.entry(full.clone()).or_default())
                }
            }
            if d.kind == "class" || d.kind == "interface" {
                for p in &d.parents {
                    if let Some(r) = &p.resolved {
                        graph.entry(full.clone()).or_default().push(r.clone())
                    }
                }
            }
            edges(&d.children, &full, graph)
        }
    }
    let mut graph = BTreeMap::new();
    for f in &model.files {
        edges(&f.declarations, &f.package, &mut graph)
    }
    fn cycle(
        n: &str,
        g: &BTreeMap<String, Vec<String>>,
        active: &mut BTreeSet<String>,
        done: &mut BTreeSet<String>,
    ) -> Result<(), String> {
        if active.contains(n) {
            return Err(format!("cyclic alias or inheritance involving {n}"));
        }
        if done.contains(n) {
            return Ok(());
        }
        active.insert(n.into());
        if let Some(es) = g.get(n) {
            for e in es {
                cycle(e, g, active, done)?
            }
        }
        active.remove(n);
        done.insert(n.into());
        Ok(())
    }
    let mut active = BTreeSet::new();
    let mut done = BTreeSet::new();
    for n in graph.keys() {
        cycle(n, &graph, &mut active, &mut done)?
    }
    let mut aliases = BTreeMap::new();
    fn collect_aliases(ds: &[Decl], scope: &str, aliases: &mut BTreeMap<String, TypeRef>) {
        for d in ds {
            let full = format!("{scope}.{}", d.name);
            if d.kind == "typealias" {
                if let Some(t) = &d.ty {
                    aliases.insert(full.clone(), t.clone());
                }
            }
            collect_aliases(&d.children, &full, aliases);
        }
    }
    for f in &model.files {
        collect_aliases(&f.declarations, &f.package, &mut aliases);
    }
    fn canonical(t: &TypeRef, aliases: &BTreeMap<String, TypeRef>) -> String {
        let mut name = t.resolved.clone().unwrap_or_else(|| t.name.clone());
        if let Some(a) = aliases.get(&name) {
            name = canonical(a, aliases);
        } else if !t.args.is_empty() {
            name.push('<');
            name.push_str(
                &t.args
                    .iter()
                    .map(|a| canonical(a, aliases))
                    .collect::<Vec<_>>()
                    .join(","),
            );
            name.push('>');
        }
        if t.nullable && !name.ends_with('?') {
            name.push('?');
        }
        name
    }
    fn validate_types(
        ds: &[Decl],
        aliases: &BTreeMap<String, TypeRef>,
        path: &str,
    ) -> Result<(), String> {
        fn nested_void(
            t: &TypeRef,
            aliases: &BTreeMap<String, TypeRef>,
            allow_void: bool,
            path: &str,
        ) -> Result<(), String> {
            let name = canonical(t, aliases);
            if (name == "Void" && !allow_void) || name == "Void?" {
                return Err(error(path, &t.span, "Void is not valid here"));
            }
            for a in &t.args {
                nested_void(a, aliases, false, path)?
            }
            if let Some(alias) = t.resolved.as_ref().and_then(|n| aliases.get(n)) {
                for a in &alias.args {
                    nested_void(a, aliases, false, path)?
                }
            }
            Ok(())
        }
        for d in ds {
            if let Some(t) = &d.ty {
                nested_void(
                    t,
                    aliases,
                    matches!(d.kind.as_str(), "fun" | "lambda" | "typealias"),
                    path,
                )?;
                if d.value.as_deref() == Some("null") && !canonical(t, aliases).ends_with('?') {
                    return Err(error(path, &t.span, "null requires a nullable type"));
                }
            }
            for p in &d.params {
                validate_types(std::slice::from_ref(p), aliases, path)?
            }
            validate_types(&d.children, aliases, path)?
        }
        Ok(())
    }
    for f in &model.files {
        validate_types(&f.declarations, &aliases, &f.path)?
    }
    let mut containers = BTreeMap::new();
    fn container_index(
        ds: &[Decl],
        scope: &str,
        out: &mut BTreeMap<String, (String, Vec<String>)>,
    ) {
        for d in ds {
            let full = format!("{scope}.{}", d.name);
            if d.kind == "class" || d.kind == "interface" {
                out.insert(full.clone(), (d.kind.clone(), d.modifiers.clone()));
            }
            container_index(&d.children, &full, out)
        }
    }
    for f in &model.files {
        container_index(&f.declarations, &f.package, &mut containers)
    }
    fn inheritance(
        ds: &[Decl],
        containers: &BTreeMap<String, (String, Vec<String>)>,
        aliases: &BTreeMap<String, TypeRef>,
        path: &str,
    ) -> Result<(), String> {
        for d in ds {
            for (i, p) in d.parents.iter().enumerate() {
                let name = canonical(p, aliases);
                let (kind, modifiers) = containers
                    .get(&name)
                    .ok_or_else(|| error(path, &p.span, "invalid inheritance target"))?;
                if d.kind == "interface" && kind != "interface" {
                    return Err(error(
                        path,
                        &p.span,
                        "interface parent must be an interface",
                    ));
                }
                if i == 0 && kind == "class" && !modifiers.iter().any(|m| m == "open") {
                    return Err(error(path, &p.span, "class parent must be open"));
                }
                if i > 0 && (kind != "interface" || !modifiers.iter().any(|m| m == "narrow")) {
                    return Err(error(
                        path,
                        &p.span,
                        "additional parents must be narrow interfaces",
                    ));
                }
            }
            inheritance(&d.children, containers, aliases, path)?
        }
        Ok(())
    }
    for f in &model.files {
        inheritance(&f.declarations, &containers, &aliases, &f.path)?
    }
    let mut hierarchy = BTreeMap::new();
    fn hierarchy_index(
        ds: &[Decl],
        scope: &str,
        aliases: &BTreeMap<String, TypeRef>,
        out: &mut BTreeMap<String, Vec<String>>,
    ) {
        for d in ds {
            let full = format!("{scope}.{}", d.name);
            if matches!(d.kind.as_str(), "class" | "interface") {
                out.insert(
                    full.clone(),
                    d.parents.iter().map(|p| canonical(p, aliases)).collect(),
                );
            }
            hierarchy_index(&d.children, &full, aliases, out)
        }
    }
    for f in &model.files {
        hierarchy_index(&f.declarations, &f.package, &aliases, &mut hierarchy)
    }
    fn ancestors(
        name: &str,
        graph: &BTreeMap<String, Vec<String>>,
        seen: &mut BTreeSet<String>,
    ) -> Result<(), String> {
        if let Some(parents) = graph.get(name) {
            for p in parents {
                if !seen.insert(p.clone()) {
                    return Err(format!("diamond inheritance involving {p}"));
                }
                ancestors(p, graph, seen)?
            }
        }
        Ok(())
    }
    for name in hierarchy.keys() {
        ancestors(name, &hierarchy, &mut BTreeSet::new())?
    }
    fn signatures(
        ds: &[Decl],
        aliases: &BTreeMap<String, TypeRef>,
        path: &str,
    ) -> Result<(), String> {
        let mut seen = BTreeSet::new();
        for d in ds {
            if matches!(d.kind.as_str(), "fun" | "constructor" | "field_constructor") {
                let signature = format!(
                    "{}({})",
                    d.name,
                    d.params
                        .iter()
                        .map(|p| p
                            .ty
                            .as_ref()
                            .map(|t| canonical(t, aliases))
                            .unwrap_or_else(|| p.name.clone()))
                        .collect::<Vec<_>>()
                        .join(",")
                );
                if !seen.insert(signature.clone()) {
                    return Err(error(
                        path,
                        &d.span,
                        &format!("duplicate signature {signature}"),
                    ));
                }
            }
            signatures(&d.children, aliases, path)?
        }
        Ok(())
    }
    for f in &model.files {
        signatures(&f.declarations, &aliases, &f.path)?
    }
    Ok(())
}

pub mod cpp;
