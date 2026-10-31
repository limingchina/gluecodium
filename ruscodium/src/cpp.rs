use crate::{Decl, Model, TypeRef};
use std::collections::BTreeSet;
fn ctype(t: &TypeRef) -> Result<String, String> {
    let args = t.args.iter().map(ctype).collect::<Result<Vec<_>, _>>()?;
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
        _ => format!(
            "::{}",
            t.resolved.as_deref().unwrap_or(&t.name).replace('.', "::")
        ),
    };
    Ok(if t.nullable {
        format!("std::optional<{s}>")
    } else {
        s
    })
}
fn emit(d: &Decl, out: &mut String, indent: &str) -> Result<(), String> {
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
    let n = d.name.trim_matches('`');
    let ty = || d.ty.as_ref().map(ctype).transpose();
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
                emit(c, out, &format!("{indent}    "))?
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
                if c.value.is_some() || !c.annotations.is_empty() {
                    return Err(format!("{}: unsupported enum metadata", c.name));
                }
                out.push_str(&format!("{indent}    {},\n", c.name));
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
                .map(|p| ctype(p.ty.as_ref().ok_or("parameter missing type")?))
                .collect::<Result<Vec<_>, String>>()?;
            out.push_str(&format!(
                "{indent}using {n} = std::function<{}({})>;\n",
                ty()?.unwrap_or("void".into()),
                ps.join(", ")
            ));
        }
        "fun" => {
            let ps = d
                .params
                .iter()
                .map(|p| {
                    Ok(format!(
                        "{} {}",
                        ctype(p.ty.as_ref().ok_or("parameter missing type")?)?,
                        p.name
                    ))
                })
                .collect::<Result<Vec<_>, String>>()?;
            let is_static = d.modifiers.iter().any(|s| s == "static");
            out.push_str(&format!(
                "{indent}{}{} {n}({}){};\n",
                if is_static { "static " } else { "virtual " },
                ty()?.unwrap_or("void".into()),
                ps.join(", "),
                if is_static { "" } else { " = 0" }
            ));
        }
        "property" => {
            let t = ty()?.ok_or("property missing type")?;
            out.push_str(&format!("{indent}virtual {t} get_{n}() const = 0;\n"));
            if d.children.iter().any(|c| c.name == "set") {
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
    let mut out=String::from("#pragma once\n#include <cstdint>\n#include <functional>\n#include <map>\n#include <optional>\n#include <set>\n#include <string>\n#include <vector>\n\n");
    let mut namespaces = BTreeSet::new();
    for f in &model.files {
        if f.auxiliary {
            continue;
        }
        namespaces.insert(f.package.clone());
    }
    for ns in namespaces {
        out.push_str(&format!("namespace {} {{\n", ns.replace('.', "::")));
        for f in &model.files {
            if !f.auxiliary && f.package == ns {
                for d in &f.declarations {
                    emit(d, &mut out, "")?
                }
            }
        }
        out.push_str("}\n");
    }
    Ok(out)
}
