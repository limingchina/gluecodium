//! Guarded whole-file C++ generation from a full JVM reference-model snapshot.
mod collect;

use crate::template::{self, native_cpp::NativeCppConfig, Graph};
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use std::{
    collections::BTreeSet,
    fs,
    path::{Component, Path, PathBuf},
};

#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub enum SourceSet {
    MAIN,
    COMMON,
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct GeneratedFile {
    pub path: PathBuf,
    pub source_set: SourceSet,
    pub contents: String,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
struct Job {
    schema: String,
    version: u64,
    snapshot: Value,
    #[serde(default)]
    raw_comments: Option<Value>,
    #[serde(default)]
    property_overlays: Option<Value>,
    #[serde(default)]
    absent_properties: Option<Value>,
    #[serde(default)]
    options: Options,
}
#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
struct Options {
    #[serde(default)]
    root_namespace: Vec<String>,
    #[serde(default)]
    internal_namespace: Vec<String>,
    #[serde(default = "default_export")]
    export: String,
    #[serde(default)]
    export_common: Option<String>,
    #[serde(default)]
    copyright_header: Option<String>,
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
fn identifier(s: &str) -> bool {
    let mut bytes = s.bytes();
    bytes
        .next()
        .is_some_and(|c| c.is_ascii_alphabetic() || c == b'_')
        && bytes.all(|c| c.is_ascii_alphanumeric() || c == b'_')
}
fn cpp_identifier(s: &str) -> bool {
    identifier(s)
        && ![
            "alignas",
            "alignof",
            "and",
            "and_eq",
            "asm",
            "auto",
            "bitand",
            "bitor",
            "bool",
            "break",
            "case",
            "catch",
            "char",
            "char16_t",
            "char32_t",
            "class",
            "compl",
            "const",
            "constexpr",
            "const_cast",
            "continue",
            "decltype",
            "default",
            "delete",
            "do",
            "double",
            "dynamic_cast",
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
            "mutable",
            "namespace",
            "new",
            "noexcept",
            "not",
            "not_eq",
            "nullptr",
            "operator",
            "or",
            "or_eq",
            "private",
            "protected",
            "public",
            "register",
            "reinterpret_cast",
            "return",
            "short",
            "signed",
            "sizeof",
            "static",
            "static_assert",
            "static_cast",
            "struct",
            "switch",
            "template",
            "this",
            "thread_local",
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
            "wchar_t",
            "while",
            "xor",
            "xor_eq",
        ]
        .contains(&s)
}
fn check_options(options: &Options) -> Result<(), String> {
    for name in options
        .root_namespace
        .iter()
        .chain(&options.internal_namespace)
        .chain([&options.export])
        .chain(options.export_common.iter())
    {
        if !cpp_identifier(name) {
            return Err(format!("invalid C++ identifier {name:?}"));
        }
    }
    Ok(())
}
pub(crate) fn validate_options(value: &Value) -> Result<(), String> {
    let options = serde_json::from_value(value.clone()).map_err(|e| format!("options: {e}"))?;
    check_options(&options)
}
fn export_file_name(name: &str, infix: &str) -> String {
    // NameHelper.toUpperCamelCase uses lower-underscore conversion when an
    // underscore is present, even when the input is already uppercase.
    let converted = if name.contains('_') {
        name.split('_')
            .filter(|s| !s.is_empty())
            .map(|part| {
                let mut c = part.chars();
                c.next()
                    .map(|first| {
                        first.to_ascii_uppercase().to_string() + &c.as_str().to_ascii_lowercase()
                    })
                    .unwrap_or_default()
            })
            .collect::<String>()
    } else if name.bytes().any(|c| c.is_ascii_lowercase())
        && name.bytes().any(|c| c.is_ascii_uppercase())
    {
        let mut c = name.chars();
        c.next()
            .map(|first| first.to_ascii_uppercase().to_string() + c.as_str())
            .unwrap_or_default()
    } else {
        let mut c = name.chars();
        c.next()
            .map(|first| first.to_ascii_uppercase().to_string() + &c.as_str().to_ascii_lowercase())
            .unwrap_or_default()
    };
    format!("Export{infix}{converted}")
}
fn class<'a>(graph: &'a Graph, value: &'a Value) -> Result<&'a str, String> {
    graph
        .class(value)
        .map(|s| s.rsplit('.').next().unwrap_or(s))
        .ok_or_else(|| format!("expected model reference: {value}"))
}
fn field(graph: &Graph, value: &Value, key: &str) -> Result<Value, String> {
    graph
        .property(value, key)?
        .ok_or_else(|| format!("missing {key} on {value}"))
}
fn array(graph: &Graph, value: &Value, key: &str) -> Result<Vec<Value>, String> {
    field(graph, value, key)?
        .as_array()
        .cloned()
        .ok_or_else(|| format!("{key} must be an array"))
}

/// Generate all files before any filesystem writes. No caller-supplied render
/// contexts or replay hooks are accepted by the job schema.
pub fn generate(templates: impl AsRef<Path>, input: &Value) -> Result<Vec<GeneratedFile>, String> {
    let job: Job =
        serde_json::from_value(input.clone()).map_err(|e| format!("generation job: {e}"))?;
    if job.schema != "gluecodium.cpp-generation-job" || ![1, 2].contains(&job.version) {
        return Err("unsupported C++ generation job schema or version".into());
    }
    if (job.version == 1 && input.get("raw_comments").is_some())
        || (job.version == 2 && job.raw_comments.is_none())
    {
        return Err("raw_comments requires generation job version 2".into());
    }
    check_options(&job.options)?;
    validate_snapshot_shape(&job.snapshot)?;
    let mut graph = Graph::import_with_absences(
        Some(&job.snapshot),
        job.property_overlays.as_ref(),
        job.absent_properties.as_ref(),
    )?;
    validate_snapshot_values(&graph, &job.snapshot)?;
    if let Some(raw) = &job.raw_comments {
        if let Some(overlays) = &job.property_overlays {
            for (id, fields) in overlays.as_object().ok_or("invalid overlays")? {
                if graph
                    .nodes
                    .get(id)
                    .is_some_and(|n| n.class.ends_with(".LimeComment"))
                    && fields.get("isEmpty").is_some()
                {
                    return Err("version 2 forbids comment isEmpty overlay".into());
                }
            }
        }
        graph.attach_raw_comments(raw)?;
        for (id, node) in &graph.nodes {
            if node.class.ends_with(".LimeComment") {
                let text = template::native_comments::selected(&graph, &json!({"$ref":id}))?
                    .ok_or("missing raw comments")?;
                template::native_comments::format(&text)?;
            }
        }
    }
    validate_graph(&graph, &job)?;
    validate_type_cycles(&graph)?;
    validate_method_names(&graph, &job.options)?;
    let root = graph.root.as_ref().ok_or("missing model root")?;
    let roots = array(&graph, root, "topElements")?;
    let config = NativeCppConfig {
        root_namespace: job.options.root_namespace.clone(),
        internal_namespace: job.options.internal_namespace.clone(),
        predicates: true,
        sorters: true,
    };
    let common_export = job
        .options
        .export_common
        .as_deref()
        .unwrap_or(&job.options.export);
    let internal = job.options.internal_namespace.join("/");
    let export_name = export_file_name(&job.options.export, "");
    let mut files = Vec::new();
    let overlays = derived_overlays(&graph, &job)?;
    let mut absences = job.absent_properties.clone().unwrap_or_else(|| json!({}));
    let absence_map = absences
        .as_object_mut()
        .ok_or("invalid absent_properties")?;
    let class_properties = graph.class_properties();
    for (id, node) in &graph.nodes {
        if node
            .class
            .starts_with("com.here.gluecodium.model.lime.Lime")
        {
            let entry = absence_map.entry(id).or_insert_with(|| json!([]));
            let values = entry.as_array_mut().ok_or("invalid absent property list")?;
            for name in ["contentTemplate", "cppRef", "cppNoexcept", "parentName"] {
                if !class_properties[&node.class].contains(name)
                    && !values.iter().any(|v| v == name)
                {
                    values.push(json!(name));
                }
            }
        }
    }
    let mut renderer = None;
    let mut render = |name: &str, data: Value| -> Result<String, String> {
        if renderer.is_none() {
            let render_graph =
                Graph::import_with_absences(Some(&job.snapshot), Some(&overlays), Some(&absences))?;
            renderer = Some(template::PreparedRenderer::new(
                templates.as_ref(),
                render_graph,
                job.raw_comments.as_ref(),
                config.clone(),
                json!(job.options.copyright_header),
                &data,
            )?);
        }
        renderer
            .as_mut()
            .expect("renderer initialized")
            .render(name, data)
    };
    let context = collect::Context::new(&graph, &config)?;
    let mut all_error_enums = BTreeSet::new();
    for root in &roots {
        for ty in context.all_types(root)? {
            if class(&graph, &ty)? == "LimeException" {
                let error = field(&graph, &ty, "errorType")?;
                all_error_enums.insert(ref_id(&field(&graph, &error, "type")?)?.to_owned());
            }
        }
    }
    for element in roots {
        let kind = class(&graph, &element)?;
        let content = match kind {
            "LimeClass" | "LimeInterface" => "cpp/CppClass",
            "LimeStruct" => "cpp/CppStruct",
            "LimeEnumeration" => "cpp/CppEnumeration",
            "LimeTypeAlias" => "cpp/CppTypeAlias",
            "LimeLambda" => "cpp/CppLambda",
            "LimeException" => continue,
            _ => return Err(format!("unsupported generation root {kind}")),
        };
        let filename = context.output(&element)?;
        let error_enums = context
            .all_types(&element)?
            .into_iter()
            .filter(|v| ref_id(v).is_ok_and(|id| all_error_enums.contains(id)))
            .collect::<Vec<_>>();
        let imports = collect::collect(&context, &element, !error_enums.is_empty())?;
        let path = field(&graph, &element, "path")?;
        let mut namespace = job.options.root_namespace.clone();
        namespace.extend(
            array(&graph, &path, "head")?
                .iter()
                .map(|v| {
                    v.as_str()
                        .map(str::to_owned)
                        .ok_or("invalid package component")
                })
                .collect::<Result<Vec<_>, _>>()?,
        );
        let mut header_includes = imports.header_includes;
        header_includes.push(collect::Include {
            file_name: join_path(&internal, &format!("{export_name}.h")),
            is_system: false,
        });
        header_includes.sort();
        header_includes.dedup();
        let header_path = format!("cpp/include/{filename}.h");
        header_includes.retain(|i| !header_path.ends_with(&i.file_name));
        let mut data = json!({"namespace":namespace,"rootNamespace":job.options.root_namespace,"internalNamespace":job.options.internal_namespace,"exportName":job.options.export,"model":element,"equatables":[],"errorEnums":error_enums,"forwardDeclarations":imports.forward_declarations,"functionUsings":{},"includes":header_includes.iter().map(|i| json!({"fileName":i.file_name,"isSystem":i.is_system})).collect::<Vec<_>>(),"contentTemplate":content});
        files.push(GeneratedFile {
            path: header_path.into(),
            source_set: SourceSet::MAIN,
            contents: render("cpp/CppHeader", data.clone())?,
        });
        if matches!(
            kind,
            "LimeClass" | "LimeInterface" | "LimeStruct" | "LimeEnumeration"
        ) {
            let mut includes = imports.implementation_includes;
            includes.push(collect::Include {
                file_name: format!("{filename}.h"),
                is_system: false,
            });
            includes.sort();
            includes.dedup();
            data["includes"] = json!(includes
                .iter()
                .map(|i| json!({"fileName":i.file_name,"isSystem":i.is_system}))
                .collect::<Vec<_>>());
            data["contentTemplate"] = json!(format!("{content}Impl"));
            files.push(GeneratedFile {
                path: format!("cpp/src/{filename}.cpp").into(),
                source_set: SourceSet::MAIN,
                contents: render("cpp/CppImplementation", data)?,
            });
        }
    }
    let common_name = export_file_name(common_export, "Common");
    let common_data = json!({"internalNamespace":job.options.internal_namespace,"exportName":common_export,"exportFileName":common_name});
    for (names, dir, suffix) in [
        (
            &[
                "DurationHash",
                "Hash",
                "Locale",
                "Optional",
                "OptionalImpl",
                "Return",
                "StringView",
                "StringViewImpl",
                "TimePointHash",
                "TypeRepository",
                "UnorderedMapHash",
                "UnorderedSetHash",
                "VectorHash",
            ][..],
            "include",
            "h",
        ),
        (
            &["LocaleImpl", "StringViewImplDefs", "TypeRepositoryImpl"][..],
            "src",
            "cpp",
        ),
    ] {
        for name in names {
            files.push(GeneratedFile {
                path: format!(
                    "cpp/{dir}/{}",
                    join_path(&internal, &format!("{name}.{suffix}"))
                )
                .into(),
                source_set: SourceSet::COMMON,
                contents: render(&format!("cpp/common/{name}"), common_data.clone())?,
            });
        }
    }
    for (macro_name, infix, source_set) in [
        (common_export, "Common", SourceSet::COMMON),
        (job.options.export.as_str(), "", SourceSet::MAIN),
    ] {
        files.push(GeneratedFile {
            path: format!(
                "cpp/include/{}",
                join_path(
                    &internal,
                    &format!("{}.h", export_file_name(macro_name, infix))
                )
            )
            .into(),
            source_set,
            contents: render(
                "cpp/common/Export",
                json!({"internalNamespace":job.options.internal_namespace,"exportName":macro_name}),
            )?,
        });
    }
    let mut seen = BTreeSet::new();
    for file in &files {
        if !safe_relative(&file.path) || !seen.insert(file.path.clone()) {
            return Err(format!(
                "unsafe or duplicate output path {}",
                file.path.display()
            ));
        }
    }
    Ok(files)
}
fn join_path(prefix: &str, suffix: &str) -> String {
    if prefix.is_empty() {
        suffix.into()
    } else {
        format!("{prefix}/{suffix}")
    }
}
fn safe_relative(path: &Path) -> bool {
    !path.as_os_str().is_empty() && path.components().all(|c| matches!(c, Component::Normal(_)))
}

/// Preflight paths and existing components before creating any directories.
/// Individual I/O failures during the subsequent write phase are reported, but
/// are not rolled back.
pub fn write_files(output: impl AsRef<Path>, files: &[GeneratedFile]) -> Result<(), String> {
    let output = output.as_ref();
    let mut seen = BTreeSet::new();
    for file in files {
        if !safe_relative(&file.path) || !seen.insert(&file.path) {
            return Err(format!(
                "unsafe or duplicate output path {}",
                file.path.display()
            ));
        }
    }
    check_no_symlinks(output)?;
    for file in files {
        check_no_symlinks(&output.join(&file.path))?;
    }
    for file in files {
        let path = output.join(&file.path);
        fs::create_dir_all(path.parent().ok_or("output path has no parent")?)
            .map_err(|e| format!("output directory: {e}"))?;
        fs::write(&path, &file.contents).map_err(|e| format!("output {}: {e}", path.display()))?;
    }
    Ok(())
}
fn check_no_symlinks(path: &Path) -> Result<(), String> {
    let mut current = PathBuf::new();
    for part in path.components() {
        match part {
            Component::Prefix(_) | Component::RootDir | Component::Normal(_) => {
                current.push(part.as_os_str())
            }
            Component::CurDir => (),
            Component::ParentDir => return Err("output path contains parent traversal".into()),
        }
        match fs::symlink_metadata(&current) {
            Ok(metadata) if metadata.file_type().is_symlink() => {
                return Err(format!(
                    "output path contains symlink {}",
                    current.display()
                ))
            }
            Ok(_) => (),
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => (),
            Err(e) => return Err(format!("output path {}: {e}", current.display())),
        }
    }
    Ok(())
}

fn validate_graph(graph: &Graph, job: &Job) -> Result<(), String> {
    let root = graph.root.as_ref().ok_or("snapshot root is required")?;
    if class(graph, root)? != "LimeModel" {
        return Err("snapshot root must be LimeModel".into());
    }
    let references = field(graph, root, "referenceMap")?;
    let references = references
        .as_object()
        .ok_or("model referenceMap must be an object")?;
    for builtin in [
        "Void", "Byte", "UByte", "Short", "UShort", "Int", "UInt", "Long", "ULong", "Float",
        "Double", "Boolean", "String", "Blob", "Date", "Duration", "Locale",
    ] {
        if !references.contains_key(builtin) {
            return Err(format!("missing builtin reference {builtin}"));
        }
    }
    let roots = array(graph, root, "topElements")?;
    let auxiliary = array(graph, root, "auxiliaryElements")?;
    let all_references: BTreeSet<String> = references
        .values()
        .map(|v| ref_id(v).map(str::to_owned))
        .collect::<Result<_, _>>()?;
    let mut owners = BTreeSet::new();
    for item in roots.iter().chain(&auxiliary) {
        let id = ref_id(item)?;
        if !owners.insert(id.to_owned()) || !all_references.contains(id) {
            return Err("duplicate or unindexed model root".into());
        }
        let path = field(graph, item, "path")?;
        if array(graph, &path, "tail")?.len() != 1 {
            return Err("model root must have exactly one container component".into());
        }
    }
    for (name, element) in references {
        let kind = class(graph, element)?;
        if kind == "LimeBasicType" {
            let expected = match name.as_str() {
                "Void" => "VOID",
                "Byte" => "INT8",
                "UByte" => "UINT8",
                "Short" => "INT16",
                "UShort" => "UINT16",
                "Int" => "INT32",
                "UInt" => "UINT32",
                "Long" => "INT64",
                "ULong" => "UINT64",
                "Float" => "FLOAT",
                "Double" => "DOUBLE",
                "Boolean" => "BOOLEAN",
                "String" => "STRING",
                "Blob" => "BLOB",
                "Date" => "DATE",
                "Duration" => "DURATION",
                "Locale" => "LOCALE",
                _ => return Err(format!("invalid builtin reference {name}")),
            };
            if field(graph, element, "typeId")?
                .get("name")
                .and_then(Value::as_str)
                != Some(expected)
            {
                return Err(format!("builtin reference {name} has wrong type"));
            }
            continue;
        }
        let path = field(graph, element, "path")?;
        let head = array(graph, &path, "head")?;
        let tail = array(graph, &path, "tail")?;
        if tail.is_empty() {
            return Err(format!("missing path for reference {name}"));
        }
        let components = head
            .iter()
            .chain(&tail)
            .map(|v| v.as_str().ok_or("non-string path component"))
            .collect::<Result<Vec<_>, _>>()?;
        let suffix = field(graph, &path, "disambiguator")?;
        let suffix = suffix.as_str().ok_or("invalid path disambiguator")?;
        let full = format!(
            "{}{}",
            components.join("."),
            if suffix.is_empty() {
                String::new()
            } else {
                format!(":{suffix}")
            }
        );
        if *name != full {
            return Err(format!("referenceMap path mismatch: {name}"));
        }
        let owner = head
            .iter()
            .chain(tail.iter().take(1))
            .map(|v| v.as_str().unwrap_or(""))
            .collect::<Vec<_>>()
            .join(".");
        let owner_ref = references
            .get(&owner)
            .ok_or_else(|| format!("missing owning root {owner}"))?;
        if !owners.contains(ref_id(owner_ref)?) {
            return Err(format!("unowned reference {name}"));
        }
        if tail.len() > 1 {
            let parent = head
                .iter()
                .chain(tail.iter().take(tail.len() - 1))
                .map(|v| v.as_str().unwrap_or(""))
                .collect::<Vec<_>>()
                .join(".");
            let parent_value = references
                .get(&parent)
                .ok_or_else(|| format!("missing parent {parent}"))?;
            let collection = match kind {
                "LimeClass" => "classes",
                "LimeInterface" => "interfaces",
                "LimeStruct" => "structs",
                "LimeEnumeration" => "enumerations",
                "LimeException" => "exceptions",
                "LimeTypeAlias" => "typeAliases",
                "LimeLambda" => "lambdas",
                "LimeConstant" => "constants",
                "LimeField" => "fields",
                "LimeFunction" => "functions",
                "LimeProperty" => "properties",
                "LimeEnumerator" => "enumerators",
                "LimeFieldConstructor" => "fieldConstructors",
                "LimeParameter" | "LimeLambdaParameter" => "parameters",
                _ => return Err(format!("unsupported indexed declaration {kind}")),
            };
            if !array(graph, parent_value, collection)?.contains(element) {
                return Err(format!(
                    "indexed declaration {name} is absent from its parent"
                ));
            }
        }
    }
    // Exception references are valid solely as the owned throws clause of an
    // ordinary indexed function. Check each use, including generic children,
    // rather than trusting a reference node merely because it is also thrown.
    let mut thrown_owners = std::collections::BTreeMap::<String, usize>::new();
    for (id, node) in &graph.nodes {
        let kind = node.class.rsplit('.').next().unwrap_or("");
        for key in [
            "typeRef",
            "errorType",
            "structRef",
            "elementType",
            "keyType",
            "valueType",
        ] {
            if let Some(reference) = node.properties.get(key) {
                if is_type_ref(class(graph, reference)?) {
                    let target = field(graph, reference, "type")?;
                    if class(graph, &target)? == "LimeException"
                        && !(kind == "LimeThrownType" && key == "typeRef")
                    {
                        return Err("exception cannot be used as a value type".into());
                    }
                }
            }
        }
        if kind == "LimeFunction" {
            let thrown = &node.properties["thrownType"];
            if !thrown.is_null() {
                *thrown_owners.entry(ref_id(thrown)?.to_owned()).or_default() += 1;
            }
        }
        if kind == "LimeThrownType" && !node.properties.contains_key("typeRef") {
            return Err(format!("invalid thrown type {id}"));
        }
    }
    for (id, node) in &graph.nodes {
        if node.class.ends_with(".LimeThrownType") && thrown_owners.get(id) != Some(&1) {
            return Err("thrown type must have exactly one function owner".into());
        }
    }
    // Measured getter views are constrained by class. Names here are LIME
    // getter names, never resolved C++ names or generator projections.
    if let Some(overlays) = &job.property_overlays {
        for (id, entries) in overlays
            .as_object()
            .ok_or("property_overlays must be an object")?
        {
            let node = graph
                .nodes
                .get(id)
                .ok_or("overlay references unknown node")?;
            let kind = node.class.rsplit('.').next().unwrap_or("");
            for (key, value) in entries.as_object().ok_or("overlay must be an object")? {
                let named = node.properties.contains_key("path")
                    && !matches!(kind, "LimePath" | "LimeComment");
                let permitted = match key.as_str() {
                    "name" | "fullName" => named,
                    "actualType" => {
                        ref_id(value).is_ok()
                            && matches!(
                                kind,
                                "LimeClass"
                                    | "LimeInterface"
                                    | "LimeStruct"
                                    | "LimeEnumeration"
                                    | "LimeException"
                                    | "LimeTypeAlias"
                                    | "LimeLambda"
                                    | "LimeBasicType"
                                    | "LimeList"
                                    | "LimeMap"
                                    | "LimeSet"
                            )
                    }
                    "isEmpty" => kind == "LimeComment",
                    "isVoid" => kind == "LimeReturnType",
                    "exception" => kind == "LimeFunction",
                    "uniqueEnumerators" => kind == "LimeEnumeration",
                    "uninitializedFields" => kind == "LimeStruct",
                    "fields" | "struct" => kind == "LimeFieldConstructor",
                    _ => false,
                };
                if !permitted {
                    return Err(format!("unsupported overlay {kind}.{key}"));
                }
                let valid = match key.as_str() {
                    "name" | "fullName" => value.is_string(),
                    "isEmpty" | "isVoid" => value.is_boolean(),
                    "exception" => value.is_null() || class(graph, value) == Ok("LimeException"),
                    "actualType" => matches!(
                        class(graph, value),
                        Ok("LimeClass"
                            | "LimeInterface"
                            | "LimeStruct"
                            | "LimeEnumeration"
                            | "LimeException"
                            | "LimeTypeAlias"
                            | "LimeLambda"
                            | "LimeBasicType"
                            | "LimeList"
                            | "LimeMap"
                            | "LimeSet")
                    ),
                    "struct" => ref_id(value).is_ok() && class(graph, value) == Ok("LimeStruct"),
                    "uniqueEnumerators" | "uninitializedFields" | "fields" => {
                        value.as_array().is_some_and(|items| {
                            items.iter().all(|item| {
                                ref_id(item).is_ok()
                                    && class(graph, item)
                                        == Ok(if key == "uniqueEnumerators" {
                                            "LimeEnumerator"
                                        } else {
                                            "LimeField"
                                        })
                            })
                        })
                    }
                    _ => false,
                };
                if !valid {
                    return Err(format!("invalid overlay value {kind}.{key}"));
                }
            }
        }
    }
    if let Some(absences) = &job.absent_properties {
        for (id, entries) in absences
            .as_object()
            .ok_or("absent_properties must be an object")?
        {
            let node = graph
                .nodes
                .get(id)
                .ok_or("absence references unknown node")?;
            let kind = node.class.rsplit('.').next().unwrap_or("");
            if !kind.starts_with("Lime")
                || matches!(
                    kind,
                    "LimeModel" | "LimePath" | "LimeAttributes" | "LimeComment"
                )
            {
                return Err(format!("unsupported absence class {kind}"));
            }
            for key in entries.as_array().ok_or("absence must be an array")? {
                let key = key.as_str().ok_or("absence must contain strings")?;
                if ![
                    "propertyElement",
                    "isVirtual",
                    "isConst",
                    "isAsyncHelper",
                    "internalNamespace",
                    "exportName",
                    "functionUsings",
                    "needsExport",
                    "storageQualifier",
                    "iter",
                    "constructorComment",
                    "struct",
                    "structElement",
                ]
                .contains(&key)
                {
                    return Err(format!("unsupported absent property {kind}.{key}"));
                }
            }
        }
    }
    for (id, node) in &graph.nodes {
        let kind = node.class.rsplit('.').next().unwrap_or("");
        let v = json!({"$ref":id});
        if !matches!(
            kind,
            "LimeModel"
                | "LimePath"
                | "LimeAttributes"
                | "LimeComment"
                | "LimeClass"
                | "LimeInterface"
                | "LimeStruct"
                | "LimeEnumeration"
                | "LimeException"
                | "LimeThrownType"
                | "LimeEnumerator"
                | "LimeTypeAlias"
                | "LimeLambda"
                | "LimeLambdaParameter"
                | "LimeFunction"
                | "LimeParameter"
                | "LimeProperty"
                | "LimeField"
                | "LimeFieldConstructor"
                | "LimeConstant"
                | "LimeReturnType"
                | "LimeBasicType"
                | "LimeList"
                | "LimeMap"
                | "LimeSet"
                | "LimeBasicTypeRef"
                | "LimeDirectTypeRef"
                | "LimeAmbiguousTypeRef"
                | "LimeLazyTypeRef"
                | "LimeLazyFieldRef"
                | "LimeValue$Literal"
                | "LimeValue$Null"
        ) {
            return Err(format!("unsupported snapshot class {kind}"));
        }
        for name in [
            "includes",
            "forwardDeclarations",
            "headerContext",
            "implementationContext",
            "contentTemplate",
            "functionUsings",
            "equatables",
            "errorEnums",
            "sortedOrder",
            "dependencies",
        ] {
            if node.properties.contains_key(name) {
                return Err(format!("generator projection {name} forbidden in snapshot"));
            }
        }
        if node
            .properties
            .get("external")
            .is_some_and(|v| !v.is_null())
        {
            return Err("external descriptors are unsupported".into());
        }
        if node
            .properties
            .get("parents")
            .is_some_and(|v| v.as_array().is_none_or(|a| !a.is_empty()))
        {
            return Err("inheritance is unsupported".into());
        }
        if matches!(kind, "LimeException" | "LimeEnumeration")
            && job
                .property_overlays
                .as_ref()
                .and_then(|o| o.get(id))
                .and_then(|o| o.get("actualType"))
                .is_some_and(|actual| actual != &v)
        {
            return Err("contradictory actualType getter".into());
        }
        if kind == "LimeException" {
            if !all_references.contains(id) {
                return Err("unindexed exception".into());
            }
            let reference = field(graph, &v, "errorType")?;
            let target = field(graph, &reference, "type")?;
            if field(graph, &reference, "isNullable")? != json!(false)
                || class(graph, &target)? != "LimeEnumeration"
                || !all_references.contains(ref_id(&target)?)
            {
                return Err(
                    "exception payload must be an indexed direct nonnullable enumeration".into(),
                );
            }
        }
        if kind == "LimeProperty" {
            for key in ["getter", "setter"] {
                let accessor = field(graph, &v, key)?;
                if !accessor.is_null() && !field(graph, &accessor, "thrownType")?.is_null() {
                    return Err("throwing property accessor is unsupported".into());
                }
            }
        }
        if kind == "LimeFunction" {
            let thrown = field(graph, &v, "thrownType")?;
            if !thrown.is_null() {
                let reference = field(graph, &thrown, "typeRef")?;
                let target = field(graph, &reference, "type")?;
                let comment = field(graph, &thrown, "comment")?;
                let comment_path = field(graph, &comment, "path")?;
                let function_path = field(graph, &v, "path")?;
                let same_path = ["head", "tail", "disambiguator"].iter().all(|key| {
                    field(graph, &comment_path, key).ok() == field(graph, &function_path, key).ok()
                });
                let empty_comment = field(graph, &comment, "isEmpty")? == json!(true)
                    && job.raw_comments.as_ref().is_none_or(|raw| {
                        raw.get(ref_id(&comment).unwrap_or(""))
                            .and_then(Value::as_array)
                            .is_some_and(Vec::is_empty)
                    });
                if !same_path
                    || !empty_comment
                    || field(graph, &comment, "isExcluded")? != json!(false)
                    || field(graph, &comment, "placeholders")? != json!({})
                {
                    return Err("throws comment must be empty and owned by its function".into());
                }
                if field(graph, &reference, "isNullable")? != json!(false)
                    || class(graph, &target)? != "LimeException"
                    || !all_references.contains(ref_id(&target)?)
                    || !all_references.contains(id)
                    || field(graph, &v, "isConstructor")? != json!(false)
                {
                    return Err("unsupported throwing function".into());
                }
            }
            let expected = if thrown.is_null() {
                Value::Null
            } else {
                let reference = field(graph, &thrown, "typeRef")?;
                field(graph, &reference, "type")?
            };
            if job
                .property_overlays
                .as_ref()
                .and_then(|v| v.get(id))
                .and_then(|v| v.get("exception"))
                .is_some_and(|supplied| supplied != &expected)
            {
                return Err("contradictory function exception getter".into());
            }
        }
        if kind == "LimeAttributes" {
            let attrs = node
                .properties
                .get("attributes")
                .and_then(Value::as_object)
                .ok_or("invalid attributes")?;
            for (group, value) in attrs {
                if group != "CPP" {
                    return Err(format!("unsupported attribute {group}"));
                }
                let cpp = value.as_object().ok_or("invalid CPP attribute")?;
                for (key, value) in cpp {
                    if key != "NAME" || !value.as_str().is_some_and(cpp_identifier) {
                        return Err(format!("unsupported or unsafe CPP attribute {key}"));
                    }
                }
            }
        }
        if job.version == 1
            && kind == "LimeComment"
            && (node.properties.get("isEmpty") != Some(&Value::Bool(true))
                || node.properties.get("isExcluded") != Some(&Value::Bool(false))
                || node
                    .properties
                    .get("placeholders")
                    .and_then(Value::as_object)
                    .is_none_or(|v| !v.is_empty()))
        {
            return Err("nonempty or unavailable documentation is unsupported".into());
        }
        if kind == "LimePath" {
            for part in array(graph, &v, "head")? {
                if !part.as_str().is_some_and(cpp_identifier) {
                    return Err("invalid package path".into());
                }
            }
            let tail = array(graph, &v, "tail")?;
            for (i, part) in tail.iter().enumerate() {
                let comment_only = job.version == 2
                    && graph
                        .nodes
                        .values()
                        .any(|owner| owner.properties.get("path") == Some(&v))
                    && graph
                        .nodes
                        .values()
                        .filter(|owner| owner.properties.get("path") == Some(&v))
                        .all(|owner| owner.class.ends_with(".LimeComment"));
                if !part.as_str().is_some_and(|s| {
                    identifier(s)
                        || (s.is_empty() && i + 1 == tail.len())
                        || (comment_only
                            && i + 1 == tail.len()
                            && s.strip_prefix('@').is_some_and(identifier))
                }) {
                    return Err("invalid declaration path".into());
                }
            }
            let suffix = field(graph, &v, "disambiguator")?;
            if !suffix
                .as_str()
                .is_some_and(|s| s.bytes().all(|b| b.is_ascii_digit()))
            {
                return Err("invalid path disambiguator".into());
            }
        }
        if kind.starts_with("LimeValue$") && !matches!(kind, "LimeValue$Literal" | "LimeValue$Null")
        {
            return Err(format!("unsupported value {kind}"));
        }
        for member in [
            "classes",
            "interfaces",
            "structs",
            "enumerations",
            "exceptions",
            "typeAliases",
            "lambdas",
            "constants",
            "fields",
            "functions",
            "properties",
            "enumerators",
            "fieldConstructors",
        ] {
            if kind == "LimeFieldConstructor" && member == "fields" {
                continue;
            }
            if let Some(items) = node.properties.get(member) {
                for child in items
                    .as_array()
                    .ok_or_else(|| format!("{kind}.{member} must be an array"))?
                {
                    if !all_references.contains(ref_id(child)?) {
                        return Err(format!("unindexed {kind}.{member} member"));
                    }
                    let parent_path = field(graph, &v, "path")?;
                    let child_path = field(graph, child, "path")?;
                    let parent_head = array(graph, &parent_path, "head")?;
                    let parent_tail = array(graph, &parent_path, "tail")?;
                    let child_head = array(graph, &child_path, "head")?;
                    let child_tail = array(graph, &child_path, "tail")?;
                    if parent_head != child_head
                        || child_tail.len() != parent_tail.len() + 1
                        || !child_tail.starts_with(&parent_tail)
                    {
                        return Err(format!("invalid owner of {kind}.{member} member"));
                    }
                }
            }
        }
    }
    Ok(())
}
fn ref_id(value: &Value) -> Result<&str, String> {
    value
        .as_object()
        .filter(|m| m.len() == 1)
        .and_then(|m| m.get("$ref"))
        .and_then(Value::as_str)
        .ok_or_else(|| "expected reference".into())
}

// Frontend getters that are functions of stored edges are recomputed here so a
// caller cannot freeze a stale declaration, constructor, or return-type view.
fn derived_overlays(graph: &Graph, job: &Job) -> Result<Value, String> {
    let mut result = job.property_overlays.clone().unwrap_or_else(|| json!({}));
    let map = result.as_object_mut().ok_or("invalid property overlays")?;
    for (id, node) in &graph.nodes {
        let kind = node.class.rsplit('.').next().unwrap_or("");
        let this = json!({"$ref":id});
        let mut updates = serde_json::Map::new();
        if node.properties.contains_key("path")
            && !matches!(
                kind,
                "LimeComment" | "LimeBasicType" | "LimeList" | "LimeMap" | "LimeSet"
            )
        {
            let path = field(graph, &this, "path")?;
            let head = array(graph, &path, "head")?;
            let tail = array(graph, &path, "tail")?;
            if let Some(name) = tail.last() {
                let suffix = field(graph, &path, "disambiguator")?;
                let suffix = suffix.as_str().ok_or("invalid disambiguator")?;
                let full = head
                    .iter()
                    .chain(&tail)
                    .map(|v| v.as_str().ok_or("invalid path"))
                    .collect::<Result<Vec<_>, _>>()?
                    .join(".");
                updates.insert("name".into(), name.clone());
                updates.insert(
                    "fullName".into(),
                    json!(if suffix.is_empty() {
                        full
                    } else {
                        format!("{full}:{suffix}")
                    }),
                );
            }
        }
        if is_type(kind) {
            let mut target = this.clone();
            let mut seen = BTreeSet::new();
            while class(graph, &target)? == "LimeTypeAlias" {
                if !seen.insert(ref_id(&target)?.to_owned()) {
                    return Err("cyclic type alias".into());
                }
                let reference = field(graph, &target, "typeRef")?;
                target = field(graph, &reference, "type")?;
            }
            updates.insert("actualType".into(), target);
        }
        match kind {
            "LimeStruct" => {
                let fields = array(graph, &this, "fields")?;
                let mut uninitialized = Vec::new();
                for item in fields {
                    if field(graph, &item, "defaultValue")?.is_null() {
                        uninitialized.push(item);
                    }
                }
                updates.insert("uninitializedFields".into(), json!(uninitialized));
            }
            "LimeEnumeration" => {
                let mut unique = Vec::new();
                for item in array(graph, &this, "enumerators")? {
                    let explicit = field(graph, &item, "explicitValue")?;
                    if explicit.is_null() || class(graph, &explicit)? != "LimeValue$Constant" {
                        unique.push(item);
                    }
                }
                updates.insert("uniqueEnumerators".into(), json!(unique));
            }
            "LimeFieldConstructor" => {
                let struct_ref = field(graph, &this, "structRef")?;
                updates.insert("struct".into(), field(graph, &struct_ref, "type")?);
                let mut fields = Vec::new();
                for f in array(graph, &this, "fieldRefs")? {
                    fields.push(field(graph, &f, "element")?);
                }
                updates.insert("fields".into(), json!(fields));
            }
            "LimeFunction" => {
                let thrown = field(graph, &this, "thrownType")?;
                let exception = if thrown.is_null() {
                    Value::Null
                } else {
                    let reference = field(graph, &thrown, "typeRef")?;
                    field(graph, &reference, "type")?
                };
                updates.insert("exception".into(), exception);
            }
            "LimeReturnType" => {
                let reference = field(graph, &this, "typeRef")?;
                let nullable = field(graph, &reference, "isNullable")?
                    .as_bool()
                    .ok_or("invalid nullability")?;
                let mut ty = field(graph, &reference, "type")?;
                let mut seen = BTreeSet::new();
                while class(graph, &ty)? == "LimeTypeAlias" {
                    if !seen.insert(ref_id(&ty)?.to_owned()) {
                        return Err("cyclic type alias".into());
                    }
                    let target = field(graph, &ty, "typeRef")?;
                    ty = field(graph, &target, "type")?;
                }
                let is_void = !nullable
                    && class(graph, &ty)? == "LimeBasicType"
                    && field(graph, &ty, "typeId")?
                        .get("name")
                        .and_then(Value::as_str)
                        == Some("VOID");
                updates.insert("isVoid".into(), json!(is_void));
            }
            _ => (),
        }
        if !updates.is_empty() {
            let target = map
                .entry(id)
                .or_insert_with(|| json!({}))
                .as_object_mut()
                .ok_or("invalid overlay")?;
            target.extend(updates);
        }
    }
    Ok(result)
}

// Reference-model snapshots expose stored Kotlin fields, not arbitrary object
// properties. Keep this closed so a field cannot shadow a generator local.
fn validate_snapshot_shape(snapshot: &Value) -> Result<(), String> {
    let snapshot = snapshot.as_object().ok_or("snapshot must be an object")?;
    if snapshot
        .keys()
        .any(|k| !["schema", "version", "root", "nodes"].contains(&k.as_str()))
    {
        return Err("unknown snapshot property".into());
    }
    for node in snapshot
        .get("nodes")
        .and_then(Value::as_array)
        .ok_or("snapshot nodes must be an array")?
    {
        let node = node.as_object().ok_or("invalid snapshot node")?;
        if node
            .keys()
            .any(|k| !["id", "class", "properties"].contains(&k.as_str()))
        {
            return Err("unknown snapshot node property".into());
        }
        let name = node
            .get("class")
            .and_then(Value::as_str)
            .ok_or("invalid node class")?;
        let kind = name
            .strip_prefix("com.here.gluecodium.model.lime.")
            .ok_or("unsupported model package")?;
        let allowed = match kind {
            "LimeModel" => "auxiliaryElements fileNameMap referenceMap topElements",
            "LimePath" => "disambiguator head tail",
            "LimeAttributes" => "attributes",
            "LimeComment" => "isExcluded path placeholders",
            "LimeClass" => "attributes childTypes classes comment constants enumerations exceptions external functions interfaces isOpen lambdas parents path properties structs typeAliases",
            "LimeInterface" => "attributes childTypes classes comment constants enumerations exceptions external functions interfaces isNarrow isOpen lambdas parents path properties structs typeAliases",
            "LimeStruct" => "attributes childTypes classes comment constants constructorComment enumerations exceptions external fieldConstructors fields functions interfaces lambdas path properties structs typeAliases",
            "LimeEnumeration" => "attributes childTypes comment enumerators external path",
            "LimeException" => "attributes childTypes comment errorType external path",
            "LimeThrownType" => "comment typeRef",
            "LimeEnumerator" => "attributes comment explicitValue external path",
            "LimeTypeAlias" => "attributes childTypes comment external path typeRef",
            "LimeLambda" => "attributes childTypes comment external parameters path returnType",
            "LimeLambdaParameter" => "attributes comment external isNamedParameter path typeRef",
            "LimeFunction" => "attributes comment external isConstructor isStatic parameters path returnType thrownType",
            "LimeParameter" => "attributes comment external path typeRef",
            "LimeProperty" => "additionalDescriptionComment attributes comment external getter isStatic path setter typeRef valueComment",
            "LimeField" => "attributes comment defaultValue external path typeRef",
            "LimeFieldConstructor" => "attributes comment external fieldRefs path structRef",
            "LimeConstant" => "attributes comment external path typeRef value",
            "LimeReturnType" => "attributes comment typeRef",
            "LimeBasicType" => "attributes childTypes comment external path typeId",
            "LimeList" | "LimeSet" => "attributes childTypes comment elementType external path",
            "LimeMap" => "attributes childTypes comment external keyType path valueType",
            "LimeBasicTypeRef" | "LimeLazyTypeRef" => "attributes element elementFullName isNullable type",
            "LimeDirectTypeRef" | "LimeAmbiguousTypeRef" => "attributes element isNullable type",
            "LimeLazyFieldRef" => "attributes element",
            "LimeValue$Literal" => "attributes typeRef value",
            "LimeValue$Null" => "attributes typeRef",
            _ => return Err(format!("unsupported snapshot class {kind}")),
        };
        let properties = node
            .get("properties")
            .and_then(Value::as_object)
            .ok_or("invalid node properties")?;
        let expected: BTreeSet<_> = allowed.split_whitespace().collect();
        let actual: BTreeSet<_> = properties.keys().map(String::as_str).collect();
        if expected != actual {
            return Err(format!(
                "invalid stored properties on {kind}: missing {:?}, unknown {:?}",
                expected.difference(&actual).collect::<Vec<_>>(),
                actual.difference(&expected).collect::<Vec<_>>()
            ));
        }
    }
    Ok(())
}

fn is_type(kind: &str) -> bool {
    matches!(
        kind,
        "LimeBasicType"
            | "LimeList"
            | "LimeMap"
            | "LimeSet"
            | "LimeClass"
            | "LimeInterface"
            | "LimeStruct"
            | "LimeEnumeration"
            | "LimeException"
            | "LimeTypeAlias"
            | "LimeLambda"
    )
}
fn is_type_ref(kind: &str) -> bool {
    matches!(
        kind,
        "LimeBasicTypeRef" | "LimeDirectTypeRef" | "LimeAmbiguousTypeRef" | "LimeLazyTypeRef"
    )
}
fn validate_snapshot_values(graph: &Graph, snapshot: &Value) -> Result<(), String> {
    for raw in snapshot["nodes"].as_array().ok_or("invalid nodes")? {
        let kind = raw["class"].as_str().unwrap().rsplit('.').next().unwrap();
        let properties = raw["properties"].as_object().ok_or("invalid properties")?;
        for (key, value) in properties {
            let target = |v: &Value, expected: &str| -> bool {
                ref_id(v).is_ok()
                    && class(graph, v).is_ok_and(|actual| match expected {
                        "type" => is_type(actual),
                        "typeRef" => is_type_ref(actual),
                        "value" => matches!(actual, "LimeValue$Literal" | "LimeValue$Null"),
                        "root" => matches!(
                            actual,
                            "LimeClass"
                                | "LimeInterface"
                                | "LimeStruct"
                                | "LimeEnumeration"
                                | "LimeException"
                                | "LimeTypeAlias"
                                | "LimeLambda"
                        ),
                        other => actual == other,
                    })
            };
            let list = |v: &Value, expected: &str| {
                v.as_array()
                    .is_some_and(|a| a.iter().all(|v| target(v, expected)))
            };
            let valid = match key.as_str() {
                "isExcluded" | "isOpen" | "isNarrow" | "isConstructor" | "isStatic"
                | "isNamedParameter" | "isNullable" => value.is_boolean(),
                "disambiguator" | "elementFullName" => value.is_string(),
                "value" if kind == "LimeValue$Literal" => value.is_string(),
                "head" | "tail" => value
                    .as_array()
                    .is_some_and(|a| a.iter().all(Value::is_string)),
                "fileNameMap" => value
                    .as_object()
                    .is_some_and(|m| m.values().all(Value::is_string)),
                "referenceMap" => value
                    .as_object()
                    .is_some_and(|m| m.values().all(|v| ref_id(v).is_ok())),
                "placeholders" | "attributes"
                    if kind == "LimeComment" || kind == "LimeAttributes" =>
                {
                    value.is_object()
                }
                "attributes" => target(value, "LimeAttributes"),
                "path" => target(value, "LimePath"),
                "comment"
                | "constructorComment"
                | "valueComment"
                | "additionalDescriptionComment" => target(value, "LimeComment"),
                "topElements" | "auxiliaryElements" => list(value, "root"),
                "childTypes" => list(value, "typeRef"),
                "classes" => list(value, "LimeClass"),
                "interfaces" => list(value, "LimeInterface"),
                "structs" => list(value, "LimeStruct"),
                "enumerations" => list(value, "LimeEnumeration"),
                "typeAliases" => list(value, "LimeTypeAlias"),
                "lambdas" => list(value, "LimeLambda"),
                "constants" => list(value, "LimeConstant"),
                "fields" => list(value, "LimeField"),
                "fieldConstructors" => list(value, "LimeFieldConstructor"),
                "functions" => list(value, "LimeFunction"),
                "properties" => list(value, "LimeProperty"),
                "enumerators" => list(value, "LimeEnumerator"),
                "parameters" => list(
                    value,
                    if kind == "LimeLambda" {
                        "LimeLambdaParameter"
                    } else {
                        "LimeParameter"
                    },
                ),
                "fieldRefs" => list(value, "LimeLazyFieldRef"),
                "parents" => value.as_array().is_some_and(Vec::is_empty),
                "exceptions" => list(value, "LimeException"),
                "typeRef" | "errorType" | "structRef" | "elementType" | "keyType" | "valueType" => {
                    target(value, "typeRef")
                }
                "returnType" => target(value, "LimeReturnType"),
                "type" => target(
                    value,
                    if kind == "LimeBasicTypeRef" {
                        "LimeBasicType"
                    } else {
                        "type"
                    },
                ),
                "element" if kind == "LimeLazyFieldRef" => target(value, "LimeField"),
                "element" => target(
                    value,
                    if kind == "LimeBasicTypeRef" {
                        "LimeBasicType"
                    } else {
                        "type"
                    },
                ),
                "getter" | "setter" => value.is_null() || target(value, "LimeFunction"),
                "explicitValue" | "defaultValue" => value.is_null() || target(value, "value"),
                "value" if kind == "LimeConstant" => target(value, "value"),
                "external" => value.is_null(),
                "thrownType" => value.is_null() || target(value, "LimeThrownType"),
                "typeId" => {
                    value.get("enum").and_then(Value::as_str)
                        == Some("com.here.gluecodium.model.lime.LimeBasicType$TypeId")
                        && value.get("name").and_then(Value::as_str).is_some_and(|v| {
                            [
                                "VOID", "INT8", "UINT8", "INT16", "UINT16", "INT32", "UINT32",
                                "INT64", "UINT64", "FLOAT", "DOUBLE", "BOOLEAN", "STRING", "BLOB",
                                "DATE", "DURATION", "LOCALE",
                            ]
                            .contains(&v)
                        })
                        && value.as_object().is_some_and(|m| m.len() == 2)
                }
                _ => false,
            };
            if !valid {
                return Err(format!("invalid stored property {kind}.{key}"));
            }
        }
        if is_type_ref(kind) && properties.get("element") != properties.get("type") {
            return Err(format!("inconsistent {kind} type and element"));
        }
        if kind == "LimeBasicTypeRef" {
            let ty = properties.get("type").ok_or("missing type")?;
            let id = field(graph, ty, "typeId")?;
            if properties.get("elementFullName").and_then(Value::as_str)
                != id.get("name").and_then(Value::as_str)
            {
                return Err("inconsistent basic type reference name".into());
            }
        }
        if let Some(children) = properties.get("childTypes") {
            let expected = match kind {
                "LimeList" | "LimeSet" => Some(vec![properties["elementType"].clone()]),
                "LimeMap" => Some(vec![
                    properties["keyType"].clone(),
                    properties["valueType"].clone(),
                ]),
                "LimeStruct" => Some(
                    properties["fields"]
                        .as_array()
                        .ok_or("invalid fields")?
                        .iter()
                        .map(|v| field(graph, v, "typeRef"))
                        .collect::<Result<Vec<_>, _>>()?,
                ),
                "LimeBasicType" => None,
                _ => Some(vec![]),
            };
            if expected.is_some_and(|v| children.as_array() != Some(&v)) {
                return Err(format!("inconsistent {kind} childTypes"));
            }
            if kind == "LimeBasicType" {
                let items = children.as_array().ok_or("invalid childTypes")?;
                let blob = properties["typeId"]["name"] == "BLOB";
                if items.len() != usize::from(blob) {
                    return Err("inconsistent basic type children".into());
                }
                if blob {
                    let ty = field(graph, &items[0], "type")?;
                    if field(graph, &ty, "typeId")?["name"] != "UINT8" {
                        return Err("invalid blob element type".into());
                    }
                }
            }
        }
    }
    Ok(())
}

fn validate_method_names(graph: &Graph, options: &Options) -> Result<(), String> {
    let config = NativeCppConfig {
        root_namespace: options.root_namespace.clone(),
        internal_namespace: options.internal_namespace.clone(),
        predicates: true,
        sorters: true,
    };
    let mut resolver = None;
    let mut resolve = |mode: &str, value: &Value| {
        if resolver.is_none() {
            resolver = Some(template::native_cpp::NativeCppResolver::new(
                graph,
                config.clone(),
            )?);
        }
        resolver
            .as_ref()
            .expect("resolver initialized")
            .resolve(graph, "", mode, value)
    };
    for (id, node) in &graph.nodes {
        let kind = node.class.rsplit('.').next().unwrap_or("");
        if matches!(kind, "LimeValue$Literal" | "LimeValue$Null") {
            let value = json!({"$ref":id});
            resolve("name", &value)?;
            if kind == "LimeValue$Literal" {
                validate_literal(graph, &value)?;
            }
        }
        if !matches!(kind, "LimeClass" | "LimeInterface" | "LimeStruct") {
            continue;
        }
        let this = json!({"$ref":id});
        let mut names = BTreeSet::new();
        for function in array(graph, &this, "functions")? {
            let name = resolve("name", &function)?.ok_or("missing function name")?;
            if !names.insert(name.clone()) {
                return Err(format!("C++ overloads unsupported: {name}"));
            }
        }
        for property in array(graph, &this, "properties")? {
            for mode in ["getter", "setter"] {
                if field(graph, &property, mode)?.is_null() {
                    continue;
                }
                let name = resolve(mode, &property)?.ok_or("missing accessor name")?;
                if !names.insert(name.clone()) {
                    return Err(format!("C++ overloads unsupported: {name}"));
                }
            }
        }
    }
    Ok(())
}

fn validate_type_cycles(graph: &Graph) -> Result<(), String> {
    fn visit(
        graph: &Graph,
        ty: &Value,
        active: &mut BTreeSet<String>,
        done: &mut BTreeSet<String>,
    ) -> Result<(), String> {
        let kind = class(graph, ty)?;
        if !matches!(kind, "LimeTypeAlias" | "LimeList" | "LimeSet" | "LimeMap") {
            return Ok(());
        }
        let id = ref_id(ty)?.to_owned();
        if done.contains(&id) {
            return Ok(());
        }
        if !active.insert(id.clone()) {
            return Err("cyclic alias or generic type".into());
        }
        if active.len() > 128 {
            return Err("type nesting limit exceeded".into());
        }
        let keys: &[&str] = match kind {
            "LimeTypeAlias" => &["typeRef"],
            "LimeList" | "LimeSet" => &["elementType"],
            "LimeMap" => &["keyType", "valueType"],
            _ => unreachable!(),
        };
        for key in keys {
            let reference = field(graph, ty, key)?;
            visit(graph, &field(graph, &reference, "type")?, active, done)?;
        }
        active.remove(&id);
        done.insert(id);
        Ok(())
    }
    let mut done = BTreeSet::new();
    for (id, node) in &graph.nodes {
        if matches!(
            node.class.rsplit('.').next().unwrap_or(""),
            "LimeTypeAlias" | "LimeList" | "LimeSet" | "LimeMap"
        ) {
            visit(graph, &json!({"$ref":id}), &mut BTreeSet::new(), &mut done)?;
        }
    }
    Ok(())
}

fn validate_literal(graph: &Graph, literal: &Value) -> Result<(), String> {
    let reference = field(graph, literal, "typeRef")?;
    let mut ty = field(graph, &reference, "type")?;
    let mut seen = BTreeSet::new();
    while class(graph, &ty)? == "LimeTypeAlias" {
        if !seen.insert(ref_id(&ty)?.to_owned()) {
            return Err("cyclic literal type".into());
        }
        let reference = field(graph, &ty, "typeRef")?;
        ty = field(graph, &reference, "type")?;
    }
    if class(graph, &ty)? != "LimeBasicType" {
        return Err("unsupported nonbasic literal".into());
    }
    let id = field(graph, &ty, "typeId")?;
    let id = id["name"].as_str().ok_or("invalid literal type")?;
    let value = field(graph, literal, "value")?;
    let text = value.as_str().ok_or("invalid literal")?;
    // Kotlin retains digit separators in the model's literal token. Validate
    // the number without changing the token passed to the templates.
    let numeric = text.replace('_', "");
    if id != "STRING"
        && text.contains('_')
        && !crate::valid_number(text.strip_prefix(['-', '+']).unwrap_or(text))
    {
        return Err("invalid numeric literal separators".into());
    }
    let valid = match id {
        "BOOLEAN" => ["true", "false"].contains(&text),
        "INT8" => numeric.parse::<i8>().is_ok(),
        "UINT8" => numeric.parse::<u8>().is_ok(),
        "INT16" => numeric.parse::<i16>().is_ok(),
        "UINT16" => numeric.parse::<u16>().is_ok(),
        "INT32" => numeric.parse::<i32>().is_ok(),
        "UINT32" => numeric.parse::<u32>().is_ok(),
        "INT64" => numeric.parse::<i64>().is_ok(),
        "UINT64" => numeric.parse::<u64>().is_ok(),
        "FLOAT" => {
            numeric.contains(['.', 'e', 'E']) && numeric.parse::<f32>().is_ok_and(f32::is_finite)
        }
        "DOUBLE" => {
            numeric.contains(['.', 'e', 'E']) && numeric.parse::<f64>().is_ok_and(f64::is_finite)
        }
        "STRING" => text
            .chars()
            .all(|c| !c.is_control() || ['\n', '\r', '\t', '\u{8}'].contains(&c)),
        _ => false,
    };
    if !valid {
        return Err(format!("unsupported or invalid {id} literal"));
    }
    Ok(())
}
