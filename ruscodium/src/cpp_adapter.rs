//! Bounded native LIME to the existing C++ compatibility generator.
mod docs;
use crate::{cpp_generation, Decl, Model, TypeRef};
use serde::{Deserialize, Serialize};
use serde_json::{json, Map, Value};
use std::{
    collections::{BTreeMap, BTreeSet},
    path::Path,
};

#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Options {
    #[serde(default)]
    pub root_namespace: Vec<String>,
    #[serde(default)]
    pub internal_namespace: Vec<String>,
    #[serde(default = "default_export")]
    pub export: String,
    #[serde(default)]
    pub export_common: Option<String>,
    #[serde(default)]
    pub copyright_header: Option<String>,
}
fn default_export() -> String {
    "_GLUECODIUM_CPP".into()
}
impl Default for Options {
    fn default() -> Self {
        Self {
            root_namespace: vec![],
            internal_namespace: vec![],
            export: default_export(),
            export_common: None,
            copyright_header: None,
        }
    }
}

const BASIC: &[(&str, &str)] = &[
    ("Blob", "BLOB"),
    ("Boolean", "BOOLEAN"),
    ("Byte", "INT8"),
    ("Date", "DATE"),
    ("Double", "DOUBLE"),
    ("Duration", "DURATION"),
    ("Float", "FLOAT"),
    ("Int", "INT32"),
    ("Locale", "LOCALE"),
    ("Long", "INT64"),
    ("Short", "INT16"),
    ("String", "STRING"),
    ("UByte", "UINT8"),
    ("UInt", "UINT32"),
    ("ULong", "UINT64"),
    ("UShort", "UINT16"),
    ("Void", "VOID"),
];
fn valid_ident(s: &str) -> bool {
    let mut c = s.chars();
    c.next()
        .is_some_and(|c| c.is_ascii_alphabetic() || c == '_')
        && c.all(|c| c.is_ascii_alphanumeric() || c == '_')
}
fn valid_qualified(s: &str) -> bool {
    !s.is_empty() && s.split('.').all(valid_ident)
}
fn guard_type(t: &mut TypeRef) -> Result<(), String> {
    if !t.docs.is_empty() {
        return Err("type-position documentation is unsupported".into());
    }
    if !t.annotations.is_empty() {
        return Err("type annotations are unsupported".into());
    }
    let builtin = BASIC.iter().any(|(n, _)| *n == t.name)
        || ["List", "Set", "Map"].contains(&t.name.as_str());
    if t.builtin != builtin || !valid_qualified(&t.name) {
        return Err(format!("invalid type reference {}", t.name));
    }
    let arity = match t.name.as_str() {
        "List" | "Set" => 1,
        "Map" => 2,
        _ => 0,
    };
    if t.args.len() != arity {
        return Err(format!("invalid type arguments for {}", t.name));
    }
    t.resolved = None;
    for arg in &mut t.args {
        guard_type(arg)?;
    }
    Ok(())
}
fn guard_decl(d: &mut Decl, parent: &str) -> Result<(), String> {
    let allowed = match parent {
        "file" => matches!(
            d.kind.as_str(),
            "class" | "interface" | "struct" | "enum" | "typealias" | "lambda"
        ),
        "class" | "interface" => matches!(
            d.kind.as_str(),
            "class"
                | "interface"
                | "struct"
                | "enum"
                | "typealias"
                | "lambda"
                | "const"
                | "fun"
                | "constructor"
                | "property"
        ),
        "struct" => matches!(
            d.kind.as_str(),
            "class"
                | "interface"
                | "struct"
                | "enum"
                | "typealias"
                | "lambda"
                | "const"
                | "fun"
                | "constructor"
                | "field"
                | "field_constructor"
        ),
        "enum" => d.kind == "enumerator",
        "fun" | "constructor" | "field_constructor" | "lambda" => d.kind == "parameter",
        "property" => d.kind == "accessor",
        _ => false,
    };
    if !allowed {
        return Err(format!("unsupported {} in {parent}", d.kind));
    }
    if !(valid_ident(&d.name) || (parent == "lambda" && d.name.is_empty())) {
        return Err(format!("invalid {} name {:?}", d.kind, d.name));
    }
    if !d.return_docs.is_empty()
        || !d.throws_docs.is_empty()
        || (matches!(d.kind.as_str(), "parameter" | "accessor") && !d.docs.is_empty())
    {
        return Err("documentation in this position is unsupported".into());
    }
    let doc = docs::parse_documentation(&d.docs)?;
    if doc
        .blocks
        .get(&("exclude".into(), String::new()))
        .is_some_and(|block| block.sections.iter().any(|(_, s)| !s.is_empty()))
    {
        return Err("@exclude does not accept text".into());
    }
    for (tag, name) in doc.blocks.keys() {
        let supported = match tag.as_str() {
            "exclude" => true,
            // The loader selects a block by the actual parameter name. A
            // recognized but unmatched @param block has no selected comment.
            "param" if matches!(d.kind.as_str(), "fun" | "constructor" | "lambda") => true,
            "return" => matches!(d.kind.as_str(), "fun" | "lambda") && d.ty.is_some(),
            "constructor" => d.kind == "struct",
            "value" | "description" | "get" | "set" => d.kind == "property",
            _ => false,
        };
        if !supported {
            return Err(format!(
                "unsupported documentation block @{tag}[{name}] on {}",
                d.kind
            ));
        }
    }
    if !d.parents.is_empty() || d.throws.is_some() || d.descriptor.is_some() {
        return Err("inheritance, throws and external descriptors are unsupported".into());
    }
    if d.modifiers.len() > 1
        || d.modifiers.iter().any(|m| {
            !matches!(
                (d.kind.as_str(), m.as_str()),
                ("class", "open")
                    | ("interface", "narrow")
                    | ("fun", "static")
                    | ("property", "static")
            )
        })
    {
        return Err("unsupported modifier".into());
    }
    if d.annotations.len() > 1
        || d.annotations.iter().any(|a| {
            a.name != "Cpp"
                || a.values.len() != 1
                || a.values[0].name.is_some()
                || a.values[0].values.len() != 1
        })
    {
        return Err("unsupported annotation".into());
    }
    if let Some(a) = d.annotations.first() {
        let source = format!("package verify\n{}\nclass Example {{}}\n", a.raw);
        let parsed = crate::parse("<annotation>", &source, false)
            .map_err(|_| "invalid annotation source")?;
        if parsed.declarations.len() != 1 {
            return Err("invalid annotation source".into());
        }
        let actual = &parsed.declarations[0].annotations;
        if actual.len() != 1
            || actual[0].raw != a.raw
            || actual[0].name != a.name
            || actual[0].values.len() != a.values.len()
            || actual[0]
                .values
                .iter()
                .zip(&a.values)
                .any(|(x, y)| x.name != y.name || x.values != y.values)
        {
            return Err("inconsistent annotation source".into());
        }
    }
    if matches!(parent, "field_constructor" | "lambda") && !d.annotations.is_empty() {
        return Err("annotations on this parameter are unsupported".into());
    }
    if !d.annotations.is_empty()
        && !matches!(
            d.kind.as_str(),
            "class"
                | "interface"
                | "struct"
                | "enum"
                | "typealias"
                | "lambda"
                | "field"
                | "fun"
                | "property"
                | "parameter"
                | "enumerator"
                | "const"
        )
    {
        return Err("unsupported annotation placement".into());
    }
    let needs_type = matches!(
        d.kind.as_str(),
        "field" | "const" | "property" | "typealias" | "lambda"
    ) || (d.kind == "parameter" && parent != "field_constructor");
    let permits_type = needs_type || d.kind == "fun";
    if needs_type && d.ty.is_none() || !permits_type && d.ty.is_some() {
        return Err(format!("invalid type on {}", d.kind));
    }
    if let Some(t) = &mut d.ty {
        guard_type(t)?;
    }
    if !matches!(
        d.kind.as_str(),
        "fun" | "constructor" | "field_constructor" | "lambda"
    ) && !d.params.is_empty()
    {
        return Err("unexpected parameters".into());
    }
    if !matches!(
        d.kind.as_str(),
        "class" | "interface" | "struct" | "enum" | "property"
    ) && !d.children.is_empty()
    {
        return Err("unexpected child declarations".into());
    }
    if matches!(d.kind.as_str(), "struct" | "enum") && d.children.is_empty() {
        return Err("empty struct or enum".into());
    }
    if d.kind == "property"
        && !(d.children.is_empty()
            || d.children.len() <= 2
                && d.children[0].name == "get"
                && (d.children.len() == 1 || d.children[1].name == "set"))
    {
        return Err("invalid property accessors".into());
    }
    if d.kind == "accessor" && !["get", "set"].contains(&d.name.as_str()) {
        return Err("invalid accessor".into());
    }
    if d.kind == "field_constructor" && d.name != "constructor" {
        return Err("invalid field constructor".into());
    }
    if d.kind == "const" && d.literal.is_none() {
        return Err("constant requires a value".into());
    }
    if !matches!(d.kind.as_str(), "const" | "field" | "enumerator")
        && (d.literal.is_some() || d.value.is_some())
    {
        return Err("unexpected literal".into());
    }
    match (&d.value, &d.literal) {
        (None, None) => (),
        (Some(v), Some(l))
            if v == &l.raw
                && l.name.is_none()
                && l.children.is_empty()
                && matches!(l.kind.as_str(), "number" | "boolean" | "string" | "null") => {}
        _ => return Err("invalid or unsupported literal".into()),
    }
    if let Some(l) = &d.literal {
        let source = format!(
            "package verify\nstruct Example {{\nvalue: Int = {}\n}}\n",
            l.raw
        );
        let parsed =
            crate::parse("<literal>", &source, false).map_err(|_| "invalid literal source")?;
        let actual = parsed.declarations[0].children[0]
            .literal
            .as_ref()
            .ok_or("missing literal")?;
        if actual.kind != l.kind || actual.raw != l.raw || !actual.children.is_empty() {
            return Err("inconsistent literal source".into());
        }
    }
    if d.kind == "enumerator" && d.literal.as_ref().is_some_and(|l| l.kind != "number") {
        return Err("unsupported enumerator value".into());
    }
    for p in &mut d.params {
        guard_decl(p, &d.kind)?;
    }
    for c in &mut d.children {
        guard_decl(c, &d.kind)?;
    }
    Ok(())
}

fn check_literal_types(model: &Model) -> Result<(), String> {
    fn aliases<'a>(decls: &'a [Decl], scope: &str, out: &mut BTreeMap<String, &'a TypeRef>) {
        for d in decls {
            let name = format!("{scope}.{}", d.name);
            if d.kind == "typealias" {
                out.insert(name.clone(), d.ty.as_ref().unwrap());
            }
            aliases(&d.children, &name, out);
        }
    }
    fn visit(decls: &[Decl], aliases: &BTreeMap<String, &TypeRef>) -> Result<(), String> {
        for d in decls {
            if let Some(l) = &d.literal {
                if d.kind == "enumerator" {
                    if l.kind != "number" {
                        return Err("invalid enumerator literal".into());
                    }
                } else {
                    let mut ty = d.ty.as_ref().ok_or("literal has no type")?;
                    let mut nullable = ty.nullable;
                    let mut visited = BTreeSet::new();
                    while let Some(next) = ty.resolved.as_ref().and_then(|r| aliases.get(r)) {
                        if !visited.insert(ty.resolved.clone()) {
                            return Err("cyclic literal alias".into());
                        }
                        ty = next;
                        nullable |= ty.nullable;
                    }
                    let expected = match ty.name.as_str() {
                        "Boolean" => "boolean",
                        "String" => "string",
                        "Byte" | "Short" | "Int" | "Long" | "UByte" | "UShort" | "UInt"
                        | "ULong" | "Float" | "Double" => "number",
                        _ => return Err("unsupported literal type".into()),
                    };
                    if l.kind != expected && !(l.kind == "null" && nullable) {
                        return Err("literal does not match its type".into());
                    }
                }
            }
            visit(&d.params, aliases)?;
            visit(&d.children, aliases)?;
        }
        Ok(())
    }
    let mut map = BTreeMap::new();
    for f in &model.files {
        aliases(&f.declarations, &f.package, &mut map);
    }
    for f in &model.files {
        visit(&f.declarations, &map)?;
    }
    Ok(())
}

struct Builder {
    nodes: Vec<Value>,
    refs: BTreeMap<String, Value>,
    raw: Map<String, Value>,
    overlays: Map<String, Value>,
    absences: Map<String, Value>,
    empty_path: Value,
}
impl Builder {
    fn new() -> Self {
        Self {
            nodes: vec![],
            refs: BTreeMap::new(),
            raw: Map::new(),
            overlays: Map::new(),
            absences: Map::new(),
            empty_path: Value::Null,
        }
    }
    fn reserve(&mut self, class: &str) -> Value {
        let id = format!("n{}", self.nodes.len() + 1);
        self.nodes.push(json!({"id":id,"class":format!("com.here.gluecodium.model.lime.{class}"),"properties":{}}));
        json!({"$ref":id})
    }
    fn set(&mut self, v: &Value, props: Value) {
        let id = v["$ref"].as_str().unwrap();
        let i = id[1..].parse::<usize>().unwrap() - 1;
        self.nodes[i]["properties"] = props;
    }
    fn node(&mut self, class: &str, props: Value) -> Value {
        let v = self.reserve(class);
        self.set(&v, props);
        v
    }
    fn path(&mut self, head: &[String], tail: &[String], suffix: &str) -> Value {
        self.node(
            "LimePath",
            json!({"head":head,"tail":tail,"disambiguator":suffix}),
        )
    }
    fn attr(&mut self, d: Option<&Decl>) -> Result<Value, String> {
        let mut a = Map::new();
        if let Some(d) = d {
            if let Some(c) = d.annotations.first() {
                let raw = &c.values[0].values[0];
                let name: String =
                    serde_json::from_str(raw).map_err(|_| "invalid Cpp annotation string")?;
                let name = name.trim().replace(['\r', '\n'], "");
                if !valid_ident(&name) {
                    return Err("invalid Cpp name".into());
                }
                a.insert("CPP".into(), json!({"NAME":name}));
            }
        }
        Ok(self.node("LimeAttributes", json!({"attributes":a})))
    }
    fn comment(&mut self, path: &Value) -> Value {
        let v = self.node(
            "LimeComment",
            json!({"isExcluded":false,"path":path,"placeholders":{}}),
        );
        self.raw
            .insert(v["$ref"].as_str().unwrap().into(), json!([]));
        v
    }
    fn comment_data(&mut self, path: &Value, data: &docs::Comment) -> Value {
        let value = self.comment(path);
        self.update_comment(&value, path, data);
        value
    }
    fn update_comment(&mut self, value: &Value, path: &Value, data: &docs::Comment) {
        let id = value["$ref"].as_str().unwrap();
        let index = id[1..].parse::<usize>().unwrap() - 1;
        self.nodes[index]["properties"]["path"] = path.clone();
        self.nodes[index]["properties"]["isExcluded"] = json!(data.is_excluded);
        self.raw.insert(id.into(), json!(data.sections));
    }
    fn empty_comment(&mut self) -> Value {
        let p = self.empty_path.clone();
        self.comment(&p)
    }
    fn basic(&mut self) -> Result<(), String> {
        for (name, _) in BASIC {
            let v = self.reserve("LimeBasicType");
            self.refs.insert((*name).into(), v);
        }
        for (name, id) in BASIC {
            let v = self.refs[*name].clone();
            let a = self.attr(None)?;
            let c = self.empty_comment();
            let child = if *name == "Blob" {
                vec![self.basic_ref("UByte", false)?]
            } else {
                vec![]
            };
            self.set(&v,json!({"attributes":a,"childTypes":child,"comment":c,"external":null,"path":self.empty_path,"typeId":{"enum":"com.here.gluecodium.model.lime.LimeBasicType$TypeId","name":id}}));
            self.overlays.insert(
                v["$ref"].as_str().unwrap().into(),
                json!({"name":name,"fullName":name,"actualType":v}),
            );
        }
        Ok(())
    }
    fn basic_ref(&mut self, name: &str, nullable: bool) -> Result<Value, String> {
        let target = self.refs.get(name).ok_or("missing basic type")?.clone();
        let a = self.attr(None)?;
        let id = BASIC.iter().find(|(n, _)| *n == name).unwrap().1;
        Ok(self.node("LimeBasicTypeRef",json!({"attributes":a,"element":target,"elementFullName":id,"isNullable":nullable,"type":target})))
    }
    fn type_ref(&mut self, t: &TypeRef) -> Result<Value, String> {
        if BASIC.iter().any(|(n, _)| *n == t.name) {
            return self.basic_ref(&t.name, t.nullable);
        }
        let target = if t.builtin {
            let args = t
                .args
                .iter()
                .map(|a| self.type_ref(a))
                .collect::<Result<Vec<_>, _>>()?;
            let attr = self.attr(None)?;
            let comment = self.empty_comment();
            let mut p = json!({"attributes":attr,"childTypes":args,"comment":comment,"external":null,"path":self.empty_path});
            if t.name == "Map" {
                p["keyType"] = args[0].clone();
                p["valueType"] = args[1].clone();
            } else {
                p["elementType"] = args[0].clone();
            }
            let v = self.node(&format!("Lime{}", t.name), p);
            self.overlays
                .insert(v["$ref"].as_str().unwrap().into(), json!({"actualType":v}));
            v
        } else {
            self.refs
                .get(t.resolved.as_ref().ok_or("unresolved type")?)
                .ok_or("missing resolved type")?
                .clone()
        };
        let a = self.attr(None)?;
        let kind = if t.builtin {
            "LimeDirectTypeRef"
        } else {
            "LimeAmbiguousTypeRef"
        };
        Ok(self.node(
            kind,
            json!({"attributes":a,"element":target,"isNullable":t.nullable,"type":target}),
        ))
    }
    fn alloc(
        &mut self,
        d: &Decl,
        head: &[String],
        tail: &[String],
        field_index: &mut usize,
    ) -> Result<(), String> {
        let mut path = tail.to_vec();
        let suffix = if d.kind == "field_constructor" {
            path.push(String::new());
            let i = *field_index;
            *field_index += 1;
            i.to_string()
        } else {
            path.push(d.name.clone());
            String::new()
        };
        let full = format!(
            "{}{}{}",
            head.iter()
                .chain(&path)
                .cloned()
                .collect::<Vec<_>>()
                .join("."),
            if suffix.is_empty() { "" } else { ":" },
            suffix
        );
        let class = match d.kind.as_str() {
            "class" => "LimeClass",
            "interface" => "LimeInterface",
            "struct" => "LimeStruct",
            "enum" => "LimeEnumeration",
            "typealias" => "LimeTypeAlias",
            "lambda" => "LimeLambda",
            "fun" | "constructor" => "LimeFunction",
            "property" => "LimeProperty",
            "field" => "LimeField",
            "const" => "LimeConstant",
            "enumerator" => "LimeEnumerator",
            "field_constructor" => "LimeFieldConstructor",
            "parameter" => "LimeParameter",
            _ => return Err("invalid declaration".into()),
        };
        let v = self.reserve(class);
        if self.refs.insert(full.clone(), v).is_some() {
            return Err(format!("duplicate declaration {full}"));
        }
        let mut nested_index = 0;
        for c in &d.children {
            if c.kind != "accessor" {
                self.alloc(c, head, &path, &mut nested_index)?;
            }
        }
        for (i, p) in d.params.iter().enumerate() {
            if d.kind != "field_constructor" {
                let mut p = p.clone();
                if d.kind == "lambda" && p.name.is_empty() {
                    p.name = format!("p{i}");
                }
                self.alloc(&p, head, &path, &mut nested_index)?;
            }
        }
        Ok(())
    }
    fn return_type(&mut self, ty: Value, comment_path: &Value) -> Result<Value, String> {
        let a = self.attr(None)?;
        let c = self.comment(comment_path);
        Ok(self.node(
            "LimeReturnType",
            json!({"attributes":a,"comment":c,"typeRef":ty}),
        ))
    }
    fn function(
        &mut self,
        path: Value,
        comment_path: &Value,
        ty: Value,
        params: Vec<Value>,
        is_static: bool,
        is_constructor: bool,
    ) -> Result<Value, String> {
        let a = self.attr(None)?;
        let c = self.comment(comment_path);
        let return_path = if params.is_empty() {
            comment_path.clone()
        } else {
            self.empty_path.clone()
        };
        let ret = self.return_type(ty, &return_path)?;
        Ok(self.node("LimeFunction",json!({"attributes":a,"comment":c,"external":null,"isConstructor":is_constructor,"isStatic":is_static,"parameters":params,"path":path,"returnType":ret,"thrownType":null})))
    }
    fn literal(&mut self, l: &crate::Literal, ty: &Value) -> Result<Value, String> {
        let a = self.attr(None)?;
        if l.kind == "null" {
            return Ok(self.node("LimeValue$Null", json!({"attributes":a,"typeRef":ty})));
        }
        let value = match l.kind.as_str() {
            "string" => {
                serde_json::from_str::<String>(&l.raw).map_err(|_| "unsupported string literal")?
            }
            "boolean" => l.raw.clone(),
            "number" => {
                let s = l.raw.trim();
                let (negative, rest) = if let Some(s) = s.strip_prefix('-') {
                    (true, s)
                } else if let Some(s) = s.strip_prefix('+') {
                    (false, s)
                } else {
                    (false, s)
                };
                format!("{}{}", if negative { "-" } else { "" }, rest.trim())
            }
            _ => return Err("unsupported literal".into()),
        };
        Ok(self.node(
            "LimeValue$Literal",
            json!({"attributes":a,"typeRef":ty,"value":value}),
        ))
    }
    fn populate(
        &mut self,
        d: &Decl,
        head: &[String],
        tail: &[String],
        field_index: &mut usize,
    ) -> Result<(), String> {
        let mut names = tail.to_vec();
        let suffix = if d.kind == "field_constructor" {
            names.push(String::new());
            let i = *field_index;
            *field_index += 1;
            i.to_string()
        } else {
            names.push(d.name.clone());
            String::new()
        };
        let key = format!(
            "{}{}{}",
            head.iter()
                .chain(&names)
                .cloned()
                .collect::<Vec<_>>()
                .join("."),
            if suffix.is_empty() { "" } else { ":" },
            suffix
        );
        let v = self
            .refs
            .get(&key)
            .ok_or_else(|| format!("missing indexed declaration {key}"))?
            .clone();
        let path = self.path(head, &names, &suffix);
        let attr = self.attr(Some(d))?;
        let doc = docs::parse_documentation(&d.docs)?;
        let comment = self.comment_data(&path, &doc.description);
        let static_ = d.modifiers.iter().any(|m| m == "static");
        let mut groups: BTreeMap<&str, Vec<Value>> = BTreeMap::new();
        let mut next = 0;
        for c in &d.children {
            if c.kind == "accessor" {
                continue;
            }
            self.populate(c, head, &names, &mut next)?;
            let mut child = names.clone();
            let suff = if c.kind == "field_constructor" {
                child.push(String::new());
                format!(":{}", next - 1)
            } else {
                child.push(c.name.clone());
                String::new()
            };
            let k = format!(
                "{}{}",
                head.iter()
                    .chain(&child)
                    .cloned()
                    .collect::<Vec<_>>()
                    .join("."),
                suff
            );
            let group = match c.kind.as_str() {
                "class" => "classes",
                "interface" => "interfaces",
                "struct" => "structs",
                "enum" => "enumerations",
                "typealias" => "typeAliases",
                "lambda" => "lambdas",
                "fun" | "constructor" => "functions",
                "property" => "properties",
                "field" => "fields",
                "const" => "constants",
                "enumerator" => "enumerators",
                "field_constructor" => "fieldConstructors",
                _ => return Err("unsupported member".into()),
            };
            groups.entry(group).or_default().push(self.refs[&k].clone());
        }
        let mut params = Vec::new();
        for (i, p) in d.params.iter().enumerate() {
            if d.kind == "field_constructor" {
                continue;
            }
            let mut p = p.clone();
            if d.kind == "lambda" && p.name.is_empty() {
                p.name = format!("p{i}");
            }
            self.populate(&p, head, &names, &mut 0)?;
            let mut n = names.clone();
            n.push(p.name.clone());
            let k = head.iter().chain(&n).cloned().collect::<Vec<_>>().join(".");
            let pv = self.refs[&k].clone();
            if d.kind == "lambda" {
                let idx = pv["$ref"].as_str().unwrap()[1..].parse::<usize>().unwrap() - 1;
                self.nodes[idx]["class"] =
                    json!("com.here.gluecodium.model.lime.LimeLambdaParameter");
                self.nodes[idx]["properties"]["isNamedParameter"] =
                    json!(!d.params[i].name.is_empty());
                let comment_id = self.nodes[idx]["properties"]["comment"]["$ref"]
                    .as_str()
                    .unwrap();
                let comment_index = comment_id[1..].parse::<usize>().unwrap() - 1;
                self.nodes[comment_index]["properties"]["path"] = path.clone();
            }
            if let Some(block) = doc
                .blocks
                .get(&("param".into(), p.name.clone()))
                .filter(|c| c.sections.iter().any(|(_, s)| !s.is_empty()))
            {
                let comment = self.nodes
                    [pv["$ref"].as_str().unwrap()[1..].parse::<usize>().unwrap() - 1]["properties"]
                    ["comment"]
                    .clone();
                let mut block_path = names.clone();
                if d.kind != "lambda" {
                    block_path.push(p.name.clone());
                }
                let block_path = self.path(head, &block_path, "");
                self.update_comment(&comment, &block_path, block);
            }
            params.push(pv);
        }
        let mut p = json!({"attributes":attr,"comment":comment,"external":null,"path":path});
        match d.kind.as_str() {
            "class" | "interface" | "struct" => {
                for group in [
                    "classes",
                    "interfaces",
                    "structs",
                    "enumerations",
                    "typeAliases",
                    "lambdas",
                    "functions",
                    "properties",
                    "constants",
                ] {
                    p[group] = json!(groups.remove(group).unwrap_or_default());
                }
                p["exceptions"] = json!([]);
                p["childTypes"] = json!([]);
                if d.kind == "struct" {
                    let fields = groups.remove("fields").unwrap_or_default();
                    let children = fields
                        .iter()
                        .map(|f| {
                            let i = f["$ref"].as_str().unwrap()[1..].parse::<usize>().unwrap() - 1;
                            self.nodes[i]["properties"]["typeRef"].clone()
                        })
                        .collect::<Vec<_>>();
                    p["fields"] = json!(fields);
                    p["childTypes"] = json!(children);
                    p["fieldConstructors"] =
                        json!(groups.remove("fieldConstructors").unwrap_or_default());
                    p["constructorComment"] = if let Some(block) = doc
                        .blocks
                        .get(&("constructor".into(), String::new()))
                        .filter(|c| c.sections.iter().any(|(_, s)| !s.is_empty()))
                    {
                        self.comment_data(&path, block)
                    } else {
                        self.empty_comment()
                    };
                } else {
                    p["parents"] = json!([]);
                    p["isOpen"] =
                        json!(d.kind == "interface" || d.modifiers.iter().any(|m| m == "open"));
                    if d.kind == "interface" {
                        p["isNarrow"] = json!(d.modifiers.iter().any(|m| m == "narrow"));
                    }
                }
            }
            "enum" => {
                p["childTypes"] = json!([]);
                p["enumerators"] = json!(groups.remove("enumerators").unwrap_or_default());
            }
            "typealias" => {
                p["childTypes"] = json!([]);
                p["typeRef"] = self.type_ref(d.ty.as_ref().unwrap())?;
            }
            "lambda" => {
                p["childTypes"] = json!([]);
                p["parameters"] = json!(params);
                let ty = self.type_ref(d.ty.as_ref().unwrap())?;
                p["returnType"] = self.return_type(ty, &path)?;
                if let Some(block) = doc
                    .blocks
                    .get(&("return".into(), String::new()))
                    .filter(|c| c.sections.iter().any(|(_, s)| !s.is_empty()))
                {
                    let mut parts = names.clone();
                    parts.push("@return".into());
                    let block_path = self.path(head, &parts, "");
                    let ret = &p["returnType"];
                    let i = ret["$ref"].as_str().unwrap()[1..].parse::<usize>().unwrap() - 1;
                    let c = self.nodes[i]["properties"]["comment"].clone();
                    self.update_comment(&c, &block_path, block);
                }
            }
            "fun" | "constructor" => {
                p["parameters"] = json!(params);
                p["isConstructor"] = json!(d.kind == "constructor");
                p["isStatic"] = json!(static_ || d.kind == "constructor");
                let ty = if d.kind == "constructor" {
                    let owner = head
                        .iter()
                        .chain(tail)
                        .cloned()
                        .collect::<Vec<_>>()
                        .join(".");
                    let target = self.refs[&owner].clone();
                    let a = self.attr(None)?;
                    self.node(
                        "LimeAmbiguousTypeRef",
                        json!({"attributes":a,"element":target,"isNullable":false,"type":target}),
                    )
                } else if let Some(t) = &d.ty {
                    self.type_ref(t)?
                } else {
                    self.basic_ref("Void", false)?
                };
                let return_path = if d.kind == "constructor" || d.ty.is_none() {
                    self.empty_path.clone()
                } else {
                    path.clone()
                };
                p["returnType"] = self.return_type(ty, &return_path)?;
                if let Some(block) = doc
                    .blocks
                    .get(&("return".into(), String::new()))
                    .filter(|c| c.sections.iter().any(|(_, s)| !s.is_empty()))
                {
                    let mut parts = names.clone();
                    parts.push("@return".into());
                    let block_path = self.path(head, &parts, "");
                    let ret = &p["returnType"];
                    let i = ret["$ref"].as_str().unwrap()[1..].parse::<usize>().unwrap() - 1;
                    let c = self.nodes[i]["properties"]["comment"].clone();
                    self.update_comment(&c, &block_path, block);
                }
                p["thrownType"] = Value::Null;
            }
            "property" => {
                let ty = self.type_ref(d.ty.as_ref().unwrap())?;
                p["typeRef"] = ty.clone();
                p["isStatic"] = json!(static_);
                let value_comment = if let Some(value) = doc
                    .blocks
                    .get(&("value".into(), String::new()))
                    .filter(|c| c.sections.iter().any(|(_, s)| !s.is_empty()))
                {
                    if doc.description.sections.iter().any(|(_, s)| !s.is_empty()) {
                        return Err("redundant property value documentation".into());
                    }
                    let mut value = value.clone();
                    value.is_excluded = doc.description.is_excluded;
                    let mut parts = names.clone();
                    parts.push("@value".into());
                    let value_path = self.path(head, &parts, "");
                    self.comment_data(&value_path, &value)
                } else {
                    let empty = docs::Comment {
                        is_excluded: doc.description.is_excluded,
                        ..Default::default()
                    };
                    self.comment_data(&path, &empty)
                };
                let description_has_text =
                    doc.description.sections.iter().any(|(_, s)| !s.is_empty());
                let accessor_comment = if description_has_text {
                    comment.clone()
                } else {
                    value_comment.clone()
                };
                p["comment"] = accessor_comment.clone();
                p["valueComment"] = value_comment;
                p["additionalDescriptionComment"] = if let Some(block) = doc
                    .blocks
                    .get(&("description".into(), String::new()))
                    .filter(|c| c.sections.iter().any(|(_, s)| !s.is_empty()))
                {
                    let mut parts = names.clone();
                    parts.push("@description".into());
                    let bp = self.path(head, &parts, "");
                    let mut block = block.clone();
                    block.is_excluded = doc.description.is_excluded;
                    self.comment_data(&bp, &block)
                } else {
                    let empty = docs::Comment {
                        is_excluded: doc.description.is_excluded,
                        ..Default::default()
                    };
                    self.comment_data(&path, &empty)
                };
                let mut get_path = names.clone();
                get_path.push("get".into());
                let getp = self.path(head, &get_path, "");
                p["getter"] = self.function(getp, &path, ty.clone(), vec![], static_, false)?;
                let getter_index = p["getter"]["$ref"].as_str().unwrap()[1..]
                    .parse::<usize>()
                    .unwrap()
                    - 1;
                let ret = self.nodes[getter_index]["properties"]["returnType"].clone();
                let ret_index = ret["$ref"].as_str().unwrap()[1..].parse::<usize>().unwrap() - 1;
                self.nodes[ret_index]["properties"]["comment"] = accessor_comment.clone();
                let getter_comment = self.nodes[getter_index]["properties"]["comment"].clone();
                let mut getter_doc = doc
                    .blocks
                    .get(&("get".into(), String::new()))
                    .cloned()
                    .unwrap_or_default();
                getter_doc.is_excluded = doc.description.is_excluded;
                let getter_path = if getter_doc.sections.iter().any(|(_, s)| !s.is_empty()) {
                    let mut parts = names.clone();
                    parts.push("@get".into());
                    self.path(head, &parts, "")
                } else {
                    path.clone()
                };
                self.update_comment(&getter_comment, &getter_path, &getter_doc);
                if d.children.is_empty() || d.children.len() == 2 {
                    let mut param_path = get_path;
                    param_path.push("value".into());
                    let pp = self.path(head, &param_path, "");
                    let pa = self.attr(None)?;
                    let pc = accessor_comment.clone();
                    let param=self.node("LimeParameter",json!({"attributes":pa,"comment":pc,"external":null,"path":pp,"typeRef":ty}));
                    let mut set_path = names.clone();
                    set_path.push("set".into());
                    let sp = self.path(head, &set_path, "");
                    let void = self.basic_ref("Void", false)?;
                    p["setter"] = self.function(sp, &path, void, vec![param], static_, false)?;
                    let setter_index = p["setter"]["$ref"].as_str().unwrap()[1..]
                        .parse::<usize>()
                        .unwrap()
                        - 1;
                    let setter_comment = self.nodes[setter_index]["properties"]["comment"].clone();
                    let mut setter_doc = doc
                        .blocks
                        .get(&("set".into(), String::new()))
                        .cloned()
                        .unwrap_or_default();
                    setter_doc.is_excluded = doc.description.is_excluded;
                    let setter_path = if setter_doc.sections.iter().any(|(_, s)| !s.is_empty()) {
                        let mut parts = names.clone();
                        parts.push("@set".into());
                        self.path(head, &parts, "")
                    } else {
                        path.clone()
                    };
                    self.update_comment(&setter_comment, &setter_path, &setter_doc);
                } else {
                    if doc.blocks.contains_key(&("set".into(), String::new())) {
                        return Err("setter documentation on readonly property".into());
                    }
                    p["setter"] = Value::Null;
                }
            }
            "parameter" => {
                p["typeRef"] = self.type_ref(d.ty.as_ref().ok_or("missing parameter type")?)?;
            }
            "field" | "const" => {
                let ty = self.type_ref(d.ty.as_ref().unwrap())?;
                p["typeRef"] = ty.clone();
                let value = if let Some(l) = &d.literal {
                    self.literal(l, &ty)?
                } else if d.kind == "field" && d.ty.as_ref().unwrap().nullable {
                    let a = self.attr(None)?;
                    self.node("LimeValue$Null", json!({"attributes":a,"typeRef":ty}))
                } else {
                    Value::Null
                };
                p[if d.kind == "field" {
                    "defaultValue"
                } else {
                    "value"
                }] = value;
            }
            "enumerator" => {
                let value = if let Some(l) = &d.literal {
                    let ty = self.basic_ref("Int", false)?;
                    self.literal(l, &ty)?
                } else {
                    Value::Null
                };
                p["explicitValue"] = value;
            }
            "field_constructor" => {
                let owner = head
                    .iter()
                    .chain(tail)
                    .cloned()
                    .collect::<Vec<_>>()
                    .join(".");
                let target = self.refs[&owner].clone();
                let a = self.attr(None)?;
                p["structRef"]=self.node("LimeLazyTypeRef",json!({"attributes":a,"element":target,"elementFullName":owner,"isNullable":false,"type":target}));
                let mut fields = Vec::new();
                for param in &d.params {
                    let key = format!("{owner}.{}", param.name);
                    let f = self
                        .refs
                        .get(&key)
                        .ok_or("unknown field constructor field")?
                        .clone();
                    let a = self.attr(None)?;
                    fields.push(self.node("LimeLazyFieldRef", json!({"attributes":a,"element":f})));
                }
                p["fieldRefs"] = json!(fields);
            }
            _ => return Err("unsupported declaration".into()),
        }
        self.set(&v, p);
        Ok(())
    }
}

/// Adapt a native model to a validated compatibility-generation job.
/// Unsupported syntax is rejected before the backend is invoked.
pub fn build_job(model: &Model, options: &Options) -> Result<Value, String> {
    cpp_generation::validate_options(&serde_json::to_value(options).map_err(|e| e.to_string())?)?;
    let mut model = model.clone();
    if model.schema_version != 1 {
        return Err("unsupported native model schema".into());
    }
    if model.files.is_empty() || model.files.iter().all(|f| f.auxiliary) {
        return Err("at least one main file is required".into());
    }
    let mut paths = BTreeSet::new();
    for f in &mut model.files {
        if f.path.is_empty()
            || !paths.insert(f.path.clone())
            || !valid_qualified(&f.package)
            || f.imports.iter().any(|i| !valid_qualified(i))
            || f.declarations.is_empty()
        {
            return Err("invalid native file metadata".into());
        }
        for d in &mut f.declarations {
            guard_decl(d, "file")?;
        }
    }
    crate::resolve(&mut model)?;
    check_literal_types(&model)?;
    let mut b = Builder::new();
    let root = b.reserve("LimeModel");
    b.empty_path = b.path(&[], &[], "");
    b.basic()?;
    for f in &model.files {
        let head = f.package.split('.').map(str::to_owned).collect::<Vec<_>>();
        let mut index = 0;
        for d in &f.declarations {
            b.alloc(d, &head, &[], &mut index)?;
        }
    }
    let mut top = Vec::new();
    let mut aux = Vec::new();
    let mut files = BTreeMap::new();
    for f in &model.files {
        let head = f.package.split('.').map(str::to_owned).collect::<Vec<_>>();
        let mut index = 0;
        for d in &f.declarations {
            b.populate(d, &head, &[], &mut index)?;
            let key = format!("{}.{}", f.package, d.name);
            let v = b.refs[&key].clone();
            if f.auxiliary {
                aux.push(v)
            } else {
                top.push(v)
            }
            files.insert(key, f.path.clone());
        }
    }
    let mut indexed = b.refs.clone();
    indexed.retain(|_, v| {
        let i = v["$ref"].as_str().unwrap()[1..].parse::<usize>().unwrap() - 1;
        !b.nodes[i]["class"]
            .as_str()
            .unwrap()
            .ends_with(".LimeLambdaParameter")
    });
    b.set(&root,json!({"auxiliaryElements":aux,"fileNameMap":files,"referenceMap":indexed,"topElements":top}));
    // Derive type views by chasing alias edges; all targets come from this graph.
    for i in 0..b.nodes.len() {
        let kind = b.nodes[i]["class"]
            .as_str()
            .unwrap()
            .rsplit('.')
            .next()
            .unwrap();
        if !matches!(
            kind,
            "LimeClass"
                | "LimeInterface"
                | "LimeStruct"
                | "LimeEnumeration"
                | "LimeLambda"
                | "LimeTypeAlias"
        ) {
            continue;
        }
        let id = b.nodes[i]["id"].as_str().unwrap().to_string();
        let mut target = json!({"$ref":id});
        let mut seen = BTreeSet::new();
        loop {
            let n = target["$ref"].as_str().ok_or("invalid alias target")?;
            if !seen.insert(n.to_string()) {
                return Err("cyclic alias".into());
            }
            let j = n[1..].parse::<usize>().map_err(|_| "invalid node")? - 1;
            if !b.nodes[j]["class"]
                .as_str()
                .unwrap()
                .ends_with(".LimeTypeAlias")
            {
                break;
            }
            let r = b.nodes[j]["properties"]["typeRef"]["$ref"]
                .as_str()
                .ok_or("invalid alias reference")?;
            let k = r[1..].parse::<usize>().map_err(|_| "invalid reference")? - 1;
            target = b.nodes[k]["properties"]["type"].clone();
        }
        b.overlays.entry(id).or_insert_with(|| json!({}))["actualType"] = target;
    }
    // These are absent getter names on the admitted model classes. The backend
    // derives its computed views separately; a stored property always wins.
    let absence_names = [
        "propertyElement",
        "isVirtual",
        "isConst",
        "isAsyncHelper",
        "internalNamespace",
        "exportName",
        "functionUsings",
        "needsExport",
        "storageQualifier",
        "structElement",
        "struct",
        "iter",
        "constructorComment",
    ];
    for n in &b.nodes {
        let kind = n["class"].as_str().unwrap().rsplit('.').next().unwrap();
        if matches!(
            kind,
            "LimeModel" | "LimePath" | "LimeAttributes" | "LimeComment"
        ) {
            continue;
        }
        let mut absent = Vec::new();
        for name in absence_names {
            if !b.nodes.iter().any(|other| {
                other["class"] == n["class"] && other["properties"].get(name).is_some()
            }) && !(kind == "LimeFieldConstructor" && name == "struct")
            {
                absent.push(name);
            }
        }
        b.absences
            .insert(n["id"].as_str().unwrap().into(), json!(absent));
    }
    Ok(
        json!({"schema":"gluecodium.cpp-generation-job","version":2,"snapshot":{"schema":"gluecodium.reference-model.snapshot","version":1,"root":root,"nodes":b.nodes},"raw_comments":b.raw,"property_overlays":b.overlays,"absent_properties":b.absences,"options":options}),
    )
}
/// Generate every file in memory using unchanged production templates.
pub fn generate(
    model: &Model,
    templates: impl AsRef<Path>,
    options: &Options,
) -> Result<Vec<cpp_generation::GeneratedFile>, String> {
    let job = build_job(model, options)?;
    cpp_generation::generate(templates, &job)
}
