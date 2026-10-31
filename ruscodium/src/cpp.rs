//! A deliberately limited standalone C++ declaration emitter.
use crate::{Decl, Model, TypeRef};
use std::collections::{BTreeMap, BTreeSet};

struct Context {
    kinds: BTreeMap<String, String>,
    tops: BTreeMap<String, String>,
    emitted: BTreeSet<String>,
}
fn identifier(s: &str) -> Result<&str, String> {
    const KEYWORDS: &[&str] = &[
        "alignas",
        "char16_t",
        "char32_t",
        "wchar_t",
        "decltype",
        "noexcept",
        "static_assert",
        "thread_local",
        "const_cast",
        "dynamic_cast",
        "reinterpret_cast",
        "static_cast",
        "mutable",
        "using",
        "compl",
        "bitand",
        "bitor",
        "and_eq",
        "or_eq",
        "xor_eq",
        "not_eq",
        "typeid",
        "char8_t",
        "alignof",
        "and",
        "asm",
        "auto",
        "bool",
        "break",
        "case",
        "catch",
        "char",
        "class",
        "const",
        "constexpr",
        "continue",
        "default",
        "delete",
        "do",
        "double",
        "else",
        "enum",
        "explicit",
        "export",
        "extern",
        "false",
        "float",
        "for",
        "friend",
        "goto",
        "if",
        "inline",
        "int",
        "long",
        "namespace",
        "new",
        "noexcept",
        "not",
        "nullptr",
        "operator",
        "or",
        "private",
        "protected",
        "public",
        "register",
        "return",
        "short",
        "signed",
        "sizeof",
        "static",
        "struct",
        "switch",
        "template",
        "this",
        "throw",
        "true",
        "try",
        "typedef",
        "typeid",
        "typename",
        "union",
        "unsigned",
        "using",
        "virtual",
        "void",
        "volatile",
        "while",
        "xor",
    ];
    if s.contains('`') {
        return Err(format!("quoted C++ identifier is unsupported: {s}"));
    }
    let s = s.trim_matches('`');
    if s.is_empty()
        || KEYWORDS.contains(&s)
        || !s
            .chars()
            .enumerate()
            .all(|(i, c)| c == '_' || c.is_ascii_alphabetic() || (i > 0 && c.is_ascii_digit()))
    {
        return Err(format!("unsupported C++ identifier {s:?}"));
    }
    Ok(s)
}
fn typecheck(
    t: &TypeRef,
    ctx: &Context,
    dependencies: &mut BTreeSet<String>,
) -> Result<(), String> {
    if t.builtin {
        let expected = match t.name.as_str() {
            "List" | "Set" => 1,
            "Map" => 2,
            _ => 0,
        };
        if t.args.len() != expected {
            return Err(format!("{}: invalid C++ type arity", t.name));
        }
    }
    if t.builtin && matches!(t.name.as_str(), "Set" | "Map") {
        let key = &t.args[0];
        let ordered_builtin = key.builtin
            && matches!(
                key.name.as_str(),
                "Byte"
                    | "Short"
                    | "Int"
                    | "Long"
                    | "UByte"
                    | "UShort"
                    | "UInt"
                    | "ULong"
                    | "Boolean"
                    | "String"
                    | "Float"
                    | "Double"
            );
        let ordered_enum = key
            .resolved
            .as_ref()
            .and_then(|n| ctx.kinds.get(n))
            .is_some_and(|k| k == "enum");
        if key.nullable || !(ordered_builtin || ordered_enum) {
            return Err(format!(
                "{}: C++ ordered container key type {} is unsupported",
                t.name, key.name
            ));
        }
    }
    if !t.annotations.is_empty() {
        return Err(format!("{}: C++ type annotations are unsupported", t.name));
    }
    for a in &t.args {
        typecheck(a, ctx, dependencies)?
    }
    if let Some(r) = &t.resolved {
        let top = ctx
            .tops
            .get(r)
            .ok_or_else(|| format!("{r}: C++ reference is unavailable"))?;
        if r != top {
            return Err(format!(
                "{r}: C++ references to nested declarations are unsupported"
            ));
        }
        if !ctx.emitted.contains(top) {
            return Err(format!(
                "{r}: C++ reference to auxiliary declaration is unsupported"
            ));
        }
        if !matches!(
            ctx.kinds.get(r).map(String::as_str),
            Some("class" | "interface")
        ) {
            dependencies.insert(top.clone());
        }
    }
    if t.builtin && ["Date", "Duration", "Locale"].contains(&t.name.as_str()) {
        return Err(format!("unsupported C++ runtime type {}", t.name));
    }
    Ok(())
}
fn ctype(t: &TypeRef, ctx: &Context) -> Result<String, String> {
    let args = t
        .args
        .iter()
        .map(|a| ctype(a, ctx))
        .collect::<Result<Vec<_>, _>>()?;
    if !t.builtin {
        let full = t
            .resolved
            .as_ref()
            .ok_or_else(|| format!("unresolved C++ type {}", t.name))?;
        let name = format!("::{}", full.replace('.', "::"));
        let mapped = if matches!(
            ctx.kinds.get(full).map(String::as_str),
            Some("class" | "interface")
        ) {
            format!("std::shared_ptr<{name}>")
        } else {
            name
        };
        return Ok(if t.nullable {
            format!("std::optional<{mapped}>")
        } else {
            mapped
        });
    }
    let s = match t.name.as_str() {
        "Void" => "void".into(),
        "Boolean" => "bool".into(),
        "Byte" => "std::int8_t".into(),
        "Short" => "std::int16_t".into(),
        "Int" => "std::int32_t".into(),
        "Long" => "std::int64_t".into(),
        "UByte" => "std::uint8_t".into(),
        "UShort" => "std::uint16_t".into(),
        "UInt" => "std::uint32_t".into(),
        "ULong" => "std::uint64_t".into(),
        "Float" => "float".into(),
        "Double" => "double".into(),
        "String" => "std::string".into(),
        "Blob" => "std::vector<std::uint8_t>".into(),
        "List" => format!("std::vector<{}>", args[0]),
        "Set" => format!("std::set<{}>", args[0]),
        "Map" => format!("std::map<{}, {}>", args[0], args[1]),
        "Date" | "Duration" | "Locale" => {
            return Err(format!("unsupported C++ runtime type {}", t.name))
        }
        _ => {
            let full = t
                .resolved
                .as_ref()
                .ok_or_else(|| format!("unresolved C++ type {}", t.name))?;
            let name = format!("::{}", full.replace('.', "::"));
            if matches!(
                ctx.kinds.get(full).map(String::as_str),
                Some("class" | "interface")
            ) {
                format!("std::shared_ptr<{name}>")
            } else {
                name
            }
        }
    };
    Ok(if t.nullable {
        format!("std::optional<{s}>")
    } else {
        s
    })
}
fn inspect(d: &Decl, ctx: &Context, deps: &mut BTreeSet<String>) -> Result<(), String> {
    if d.kind != "parameter" || !d.name.is_empty() {
        identifier(&d.name)?;
    }
    if !d.annotations.is_empty() || d.descriptor.is_some() || d.throws.is_some() {
        return Err(format!(
            "{}: C++ backend does not support annotations, external descriptors or throws",
            d.name
        ));
    }
    if d.value.is_some() {
        return Err(format!(
            "{}: C++ backend does not support initializers",
            d.name
        ));
    }
    if !d.parents.is_empty() {
        return Err(format!(
            "{}: C++ backend does not support inheritance",
            d.name
        ));
    }
    if let Some(t) = &d.ty {
        typecheck(t, ctx, deps)?
    }
    for p in &d.params {
        inspect(p, ctx, deps)?
    }
    if matches!(d.kind.as_str(), "class" | "interface" | "struct") {
        let mut names = BTreeSet::new();
        let mut functions: BTreeMap<String, BTreeSet<Vec<String>>> = BTreeMap::new();
        for c in &d.children {
            if d.kind == "struct" && c.kind == "fun" && !c.modifiers.iter().any(|m| m == "static") {
                return Err(format!(
                    "{}: struct instance methods are unsupported",
                    c.name
                ));
            }
            if matches!(c.kind.as_str(), "fun" | "constructor") {
                if names.contains(&c.name) {
                    return Err(format!("{}: generated C++ member name collision", c.name));
                }
                let args = c
                    .params
                    .iter()
                    .map(|p| ctype(p.ty.as_ref().ok_or("parameter missing type")?, ctx))
                    .collect::<Result<Vec<_>, String>>()?;
                if !functions.entry(c.name.clone()).or_default().insert(args) {
                    return Err(format!("{}: generated C++ signature collision", c.name));
                }
                continue;
            }
            let generated: Vec<String> = if c.kind == "property" {
                let mut v = vec![format!("get_{}", c.name)];
                if c.children.is_empty() || c.children.iter().any(|a| a.name == "set") {
                    v.push(format!("set_{}", c.name));
                }
                v
            } else {
                vec![c.name.clone()]
            };
            for name in generated {
                if functions.contains_key(&name) || !names.insert(name.clone()) {
                    return Err(format!("{name}: generated C++ member name collision"));
                }
            }
        }
    }
    for c in &d.children {
        inspect(c, ctx, deps)?
    }
    Ok(())
}
fn emit(
    d: &Decl,
    out: &mut String,
    indent: &str,
    ctx: &Context,
    owner: Option<&str>,
) -> Result<(), String> {
    let n = identifier(&d.name)?;
    if owner == Some(n) {
        return Err(format!("{n}: member name conflicts with its C++ class"));
    }
    let ty = || d.ty.as_ref().map(|t| ctype(t, ctx)).transpose();
    match d.kind.as_str() {
        "struct" | "class" | "interface" => {
            out.push_str(&format!(
                "{indent}{} {n} {{\n",
                if d.kind == "struct" {
                    "struct"
                } else {
                    "class"
                }
            ));
            if d.kind != "struct" {
                out.push_str(&format!(
                    "{indent}public:\n{indent}    virtual ~{n}() = default;\n"
                ));
            }
            for c in &d.children {
                emit(c, out, &format!("{indent}    "), ctx, Some(n))?
            }
            out.push_str(&format!("{indent}}};\n"));
        }
        "field" => out.push_str(&format!(
            "{indent}{} {n};\n",
            ty()?.ok_or("field missing type")?
        )),
        "enum" => {
            out.push_str(&format!("{indent}enum class {n} {{\n"));
            for c in &d.children {
                out.push_str(&format!("{indent}    {},\n", identifier(&c.name)?));
            }
            out.push_str(&format!("{indent}}};\n"));
        }
        "typealias" => out.push_str(&format!(
            "{indent}using {n} = {};\n",
            ty()?.ok_or("alias missing type")?
        )),
        "lambda" => {
            let ps = d
                .params
                .iter()
                .map(|p| ctype(p.ty.as_ref().ok_or("parameter missing type")?, ctx))
                .collect::<Result<Vec<_>, String>>()?;
            out.push_str(&format!(
                "{indent}using {n} = std::function<{}({})>;\n",
                ty()?.unwrap_or("void".into()),
                ps.join(", ")
            ));
        }
        "fun" | "constructor" => {
            let ps = d
                .params
                .iter()
                .map(|p| {
                    Ok(format!(
                        "{} {}",
                        ctype(p.ty.as_ref().ok_or("parameter missing type")?, ctx)?,
                        identifier(&p.name)?
                    ))
                })
                .collect::<Result<Vec<_>, String>>()?;
            let is_static = d.modifiers.iter().any(|s| s == "static") || d.kind == "constructor";
            let ret = if d.kind == "constructor" {
                format!(
                    "std::shared_ptr<{}>",
                    owner.ok_or("constructor outside container")?
                )
            } else {
                ty()?.unwrap_or("void".into())
            };
            out.push_str(&format!(
                "{indent}{}{ret} {n}({}){};\n",
                if is_static { "static " } else { "virtual " },
                ps.join(", "),
                if is_static { "" } else { " = 0" }
            ));
        }
        "property" => {
            let t = ty()?.ok_or("property missing type")?;
            if d.modifiers.iter().any(|s| s == "static") {
                return Err("static properties are unsupported".into());
            }
            out.push_str(&format!("{indent}virtual {t} get_{n}() const = 0;\n"));
            if d.children.is_empty() || d.children.iter().any(|c| c.name == "set") {
                out.push_str(&format!("{indent}virtual void set_{n}({t} value) = 0;\n"));
            }
        }
        _ => {
            return Err(format!(
                "{}: unsupported C++ declaration {}",
                d.name, d.kind
            ))
        }
    }
    Ok(())
}
pub fn generate(model: &Model) -> Result<String, String> {
    fn index(ds: &[Decl], scope: &str, top: Option<&str>, ctx: &mut Context) {
        for d in ds {
            if matches!(
                d.kind.as_str(),
                "class" | "interface" | "struct" | "enum" | "typealias" | "lambda" | "exception"
            ) {
                let full = format!("{scope}.{}", d.name);
                let root = top.unwrap_or(&full);
                ctx.kinds.insert(full.clone(), d.kind.clone());
                ctx.tops.insert(full.clone(), root.into());
                index(&d.children, &full, Some(root), ctx)
            }
        }
    }
    let mut ctx = Context {
        kinds: BTreeMap::new(),
        tops: BTreeMap::new(),
        emitted: BTreeSet::new(),
    };
    let mut all = BTreeMap::new();
    for f in &model.files {
        for part in f.package.split('.') {
            identifier(part)?;
        }
        index(&f.declarations, &f.package, None, &mut ctx);
        if !f.auxiliary {
            for d in &f.declarations {
                let name = format!("{}.{}", f.package, d.name);
                ctx.emitted.insert(name.clone());
                all.insert(name, (f.package.as_str(), d));
            }
        }
    }
    for f in &model.files {
        if !f.auxiliary {
            let mut prefix = String::new();
            for part in f.package.split('.') {
                if !prefix.is_empty() {
                    prefix.push('.')
                }
                prefix.push_str(part);
                if ctx.emitted.contains(&prefix) {
                    return Err(format!("{prefix}: C++ namespace conflicts with a type"));
                }
            }
        }
    }
    let mut graph = BTreeMap::new();
    for (name, (_, d)) in &all {
        let mut deps = BTreeSet::new();
        inspect(d, &ctx, &mut deps)?;
        if deps.contains(name) && d.kind != "class" && d.kind != "interface" {
            return Err(format!("{name}: cyclic C++ value dependency"));
        }
        deps.remove(name);
        graph.insert(name.clone(), deps);
    }
    let mut ordered = Vec::new();
    let mut remaining: BTreeSet<_> = all.keys().cloned().collect();
    while !remaining.is_empty() {
        let next = remaining
            .iter()
            .find(|n| graph[*n].is_disjoint(&remaining))
            .cloned()
            .ok_or("C++ declarations have cyclic by-value dependencies")?;
        remaining.remove(&next);
        ordered.push(next);
    }
    let mut out=String::from("#pragma once\n#include <cstdint>\n#include <functional>\n#include <map>\n#include <memory>\n#include <optional>\n#include <set>\n#include <string>\n#include <vector>\n\n");
    for f in &model.files {
        if !f.auxiliary {
            for d in &f.declarations {
                if matches!(d.kind.as_str(), "class" | "interface" | "struct") {
                    out.push_str(&format!(
                        "namespace {} {{ {} {}; }}\n",
                        f.package.replace('.', "::"),
                        if d.kind == "struct" {
                            "struct"
                        } else {
                            "class"
                        },
                        identifier(&d.name)?
                    ));
                }
            }
        }
    }
    for name in ordered {
        let (ns, d) = all[&name];
        out.push_str(&format!("namespace {} {{\n", ns.replace('.', "::")));
        emit(d, &mut out, "", &ctx, None)?;
        out.push_str("}\n");
    }
    Ok(out)
}
