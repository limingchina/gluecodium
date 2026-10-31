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
pub struct TypeRef {
    pub name: String,
    pub args: Vec<TypeRef>,
    pub nullable: bool,
    pub annotations: Vec<String>,
    pub span: Span,
    pub resolved: Option<String>,
}
#[derive(Debug, Clone, Serialize)]
pub struct Decl {
    pub kind: String,
    pub name: String,
    pub span: Span,
    pub docs: Vec<String>,
    pub annotations: Vec<String>,
    pub modifiers: Vec<String>,
    pub ty: Option<TypeRef>,
    pub parents: Vec<TypeRef>,
    pub params: Vec<Decl>,
    pub children: Vec<Decl>,
    pub value: Option<String>,
    pub descriptor: Option<String>,
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

pub fn lex(path: &str, src: &str) -> Result<Vec<Token>, String> {
    let mut out = Vec::new();
    let mut i = 0;
    let mut line = 1;
    let mut col = 1;
    while i < src.len() {
        let start = i;
        let sl = line;
        let sc = col;
        let tail = &src[i..];
        let c = tail.chars().next().unwrap();
        let (n, kind) = if c.is_whitespace() {
            (c.len_utf8(), "space")
        } else if c == '#' {
            (tail.find('\n').unwrap_or(tail.len()), "space")
        } else if tail.starts_with("//") {
            (tail.find('\n').unwrap_or(tail.len()), "doc")
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
        } else if c.is_ascii_digit() {
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
            if ch == '\n' {
                line += 1;
                col = 1
            } else {
                col += 1
            }
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
            Ok(self.next())
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
    fn meta(&mut self) -> Result<(Vec<String>, Vec<String>), String> {
        let mut docs = Vec::new();
        let mut attrs = Vec::new();
        loop {
            if self.t[self.i].kind == "doc" {
                docs.push(self.next())
            } else if self.eat("@") {
                let start = self.t[self.i - 1].span.start;
                self.id()?;
                if self.eat("(") {
                    loop {
                        if self.t[self.i].kind == "string" {
                            self.next();
                        } else {
                            self.id()?;
                            if self.eat("=") {
                                if self.eat("[") {
                                    loop {
                                        self.string()?;
                                        if !self.eat(",") {
                                            break;
                                        }
                                    }
                                    self.expect("]")?;
                                } else {
                                    self.string()?;
                                }
                            }
                        }
                        if !self.eat(",") {
                            break;
                        }
                    }
                    self.expect(")")?;
                }
                let end = self.t[self.i - 1].span.end;
                attrs.push(self.src[start..end].into());
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
        let name = if BUILTINS.contains(&self.peek()) {
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
            descriptor: None,
            throws: None,
            return_docs: Vec::new(),
            throws_docs: Vec::new(),
        };
        match kind.as_str() {
            "class" | "interface" | "struct" | "enum" => {
                if self.eat(":") {
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
                if self.eat(":") {
                    let (docs, attrs) = self.meta()?;
                    d.return_docs = docs;
                    let mut ty = self.typ()?;
                    ty.annotations.splice(0..0, attrs);
                    d.ty = Some(ty)
                }
                if self.eat("throws") {
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
                if self.eat("=") {
                    d.value = Some(self.literal()?)
                }
                if self.peek() == "external" {
                    d.descriptor = Some(self.descriptor()?)
                }
                if kind == "property" && self.eat("{") {
                    while self.peek() != "}" {
                        let (docs, annotations) = self.meta()?;
                        let span = self.span();
                        let name = self.next();
                        if name != "get" && name != "set" {
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
                            descriptor,
                            throws: None,
                            return_docs: Vec::new(),
                            throws_docs: Vec::new(),
                        })
                    }
                    self.expect("}")?;
                }
            }
            "enumerator" => {
                if self.eat("=") {
                    d.value = Some(self.literal()?)
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
    fn descriptor(&mut self) -> Result<String, String> {
        let start = self.span().start;
        self.expect("external")?;
        self.expect("{")?;
        let mut count = 0;
        while self.peek() != "}" {
            self.id()?;
            self.id()?;
            self.string()?;
            count += 1;
        }
        if count == 0 {
            return Err(error(
                self.path,
                &self.span(),
                "expected external descriptor value",
            ));
        }
        self.expect("}")?;
        Ok(self.src[start..self.t[self.i - 1].span.end].into())
    }
    fn literal(&mut self) -> Result<String, String> {
        let start = self.span().start;
        if self.eat("{") {
            if self.peek() != "}" {
                loop {
                    if self.t.get(self.i + 1).is_some_and(|t| t.text == "=") {
                        self.id()?;
                        self.expect("=")?;
                    }
                    self.literal()?;
                    if !self.eat(",") {
                        break;
                    }
                }
            }
            self.expect("}")?;
        } else if self.eat("[") {
            if self.peek() != "]" {
                loop {
                    self.literal()?;
                    if self.eat(":") {
                        self.literal()?;
                    }
                    if !self.eat(",") {
                        break;
                    }
                }
            }
            self.expect("]")?;
        } else {
            let signed = self.eat("+") || self.eat("-");
            if !["id", "number", "string"].contains(&self.t[self.i].kind.as_str()) {
                return Err(error(self.path, &self.span(), "expected literal"));
            }
            if signed && self.t[self.i].kind != "number" && self.peek() != "Infinity" {
                return Err(error(self.path, &self.span(), "expected numeric literal"));
            }
            self.next();
            while self.eat(".") {
                self.id()?;
            }
            if self.eat("(") {
                if self.t[self.i].kind != "number" {
                    return Err(error(self.path, &self.span(), "expected integer"));
                }
                self.next();
                self.expect(")")?;
            }
        }
        Ok(self.src[start..self.t[self.i - 1].span.end].into())
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
    fn walk(p: &Path, out: &mut BTreeSet<PathBuf>) -> Result<(), String> {
        if p.is_dir() {
            let entries = fs::read_dir(p).map_err(|e| format!("{}: {e}", p.display()))?;
            for entry in entries {
                walk(&entry.map_err(|e| e.to_string())?.path(), out)?
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
    for p in paths {
        walk(p, &mut out)?
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
        if BUILTINS.contains(&t.name.as_str()) {
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
                if (t.name == "Void" && d.kind != "fun" && d.kind != "lambda")
                    || (t.name == "Void" && t.nullable)
                {
                    return Err(error(path, &t.span, "Void is not valid here"));
                }
                if t.nullable && d.value.as_deref() == Some("null") {
                } else if !t.nullable && d.value.as_deref() == Some("null") {
                    return Err(error(path, &t.span, "null requires a nullable type"));
                }
            }
            for t in &mut d.parents {
                ty(t, scope, imports, symbols, path)?;
                let kind = t.resolved.as_ref().and_then(|n| symbols.get(n));
                if !matches!(kind.map(String::as_str), Some("class" | "interface"))
                    || (d.kind == "interface" && kind.map(String::as_str) != Some("interface"))
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
        if t.nullable {
            name.push('?');
        }
        name
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
