//! Dependency collection for the guarded native C++ generator.
use crate::template::{
    native_cpp::{NativeCppConfig, NativeCppResolver},
    Graph,
};
use serde_json::{json, Value};
use std::{
    cell::RefCell,
    collections::{BTreeMap, BTreeSet},
};

#[derive(Clone, Debug, PartialEq, Eq)]
pub(super) struct Include {
    pub file_name: String,
    pub is_system: bool,
}
impl Ord for Include {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.is_system
            .cmp(&other.is_system)
            .then_with(|| self.file_name.cmp(&other.file_name))
    }
}
impl PartialOrd for Include {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}
pub(super) struct Collected {
    pub header_includes: Vec<Include>,
    pub implementation_includes: Vec<Include>,
    pub forward_declarations: Value,
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
struct ModelPath {
    head: Vec<String>,
    tail: Vec<String>,
    disambiguator: String,
}
impl ModelPath {
    fn text(&self) -> String {
        let mut s = self
            .head
            .iter()
            .chain(&self.tail)
            .cloned()
            .collect::<Vec<_>>()
            .join(".");
        if !self.disambiguator.is_empty() {
            s.push(':');
            s.push_str(&self.disambiguator);
        }
        s
    }
    fn parent(&self) -> Self {
        let mut p = self.clone();
        p.tail.pop();
        p.disambiguator.clear();
        p
    }
}
pub(super) struct Context<'a> {
    graph: &'a Graph,
    config: &'a NativeCppConfig,
    paths: BTreeMap<ModelPath, Vec<Value>>,
    resolver: RefCell<Option<NativeCppResolver>>,
}
impl<'a> Context<'a> {
    pub(super) fn new(graph: &'a Graph, config: &'a NativeCppConfig) -> Result<Self, String> {
        let mut c = Self {
            graph,
            config,
            paths: BTreeMap::new(),
            resolver: RefCell::new(None),
        };
        for (id, n) in &graph.nodes {
            if n.properties.contains_key("path")
                && n.properties.contains_key("attributes")
                && n.properties.contains_key("external")
            {
                let v = json!({"$ref":id});
                let p = c.path(&v)?;
                c.paths.entry(p).or_default().push(v);
            }
        }
        Ok(c)
    }
    fn get(&self, v: &Value, key: &str) -> Result<Value, String> {
        self.graph
            .property(v, key)?
            .ok_or_else(|| format!("missing {key} on {v}"))
    }
    fn class<'b>(&'b self, v: &'b Value) -> Result<&'b str, String> {
        self.graph
            .class(v)
            .map(|s| s.rsplit('.').next().unwrap_or(s))
            .ok_or_else(|| format!("expected model node: {v}"))
    }
    fn array(&self, v: &Value, key: &str) -> Result<Vec<Value>, String> {
        self.get(v, key)?
            .as_array()
            .cloned()
            .ok_or_else(|| format!("invalid {key} array"))
    }
    fn path(&self, v: &Value) -> Result<ModelPath, String> {
        let p = self.get(v, "path")?;
        let list = |key| -> Result<Vec<String>, String> {
            self.array(&p, key)?
                .iter()
                .map(|x| {
                    x.as_str()
                        .map(str::to_owned)
                        .ok_or_else(|| format!("invalid path {key}"))
                })
                .collect()
        };
        Ok(ModelPath {
            head: list("head")?,
            tail: list("tail")?,
            disambiguator: self
                .get(&p, "disambiguator")?
                .as_str()
                .ok_or("invalid path disambiguator")?
                .into(),
        })
    }
    fn root(&self, v: &Value) -> Result<Value, String> {
        let mut p = self.path(v)?;
        if p.tail.is_empty() {
            return Err("empty named type path".into());
        }
        while p.tail.len() > 1 {
            p = p.parent();
        }
        match self.paths.get(&p).map(Vec::as_slice) {
            Some([v]) => Ok(v.clone()),
            Some(_) => Err(format!("duplicate native C++ path {}", p.text())),
            None => Err(format!("missing native C++ owning root {}", p.text())),
        }
    }
    fn name(&self, v: &Value) -> Result<String, String> {
        let mut resolver = self.resolver.borrow_mut();
        if resolver.is_none() {
            *resolver = Some(NativeCppResolver::new(self.graph, self.config.clone())?);
        }
        resolver
            .as_ref()
            .expect("resolver initialized")
            .resolve(self.graph, "C++", "name", v)?
            .ok_or_else(|| "missing native C++ name".into())
    }
    pub(super) fn output(&self, v: &Value) -> Result<String, String> {
        let root = self.root(v)?;
        let p = self.path(&root)?;
        let name = self.name(&root)?;
        let mut pieces = self.config.root_namespace.clone();
        pieces.extend(p.head);
        pieces.push(name);
        Ok(pieces.join("/"))
    }
    fn inc(&self, v: &Value) -> Result<Include, String> {
        Ok(Include {
            file_name: format!("{}.h", self.output(v)?),
            is_system: false,
        })
    }
    fn internal(&self, name: &str) -> Include {
        let mut p = self.config.internal_namespace.clone();
        p.push(name.into());
        Include {
            file_name: p.join("/"),
            is_system: false,
        }
    }
    fn system(name: &str) -> Include {
        Include {
            file_name: name.into(),
            is_system: true,
        }
    }
    fn attrs(&self, v: &Value) -> Result<serde_json::Map<String, Value>, String> {
        let attrs = self.get(v, "attributes")?;
        let id = attrs
            .get("$ref")
            .and_then(Value::as_str)
            .ok_or("invalid attributes reference")?;
        self.graph
            .nodes
            .get(id)
            .and_then(|n| n.properties.get("attributes"))
            .and_then(Value::as_object)
            .cloned()
            .ok_or_else(|| "invalid attributes".into())
    }
    fn actual(&self, v: &Value) -> Result<Value, String> {
        let mut v = v.clone();
        let mut seen = BTreeSet::new();
        while self.class(&v)? == "LimeTypeAlias" {
            if !seen.insert(v.to_string()) || seen.len() > 128 {
                return Err("cyclic C++ alias".into());
            }
            v = self.get(&self.get(&v, "typeRef")?, "type")?;
        }
        Ok(v)
    }
    fn refs_children(
        &self,
        r: &Value,
        out: &mut Vec<Value>,
        active: &mut BTreeSet<String>,
    ) -> Result<(), String> {
        let key = r.to_string();
        if !active.insert(key.clone()) || active.len() > 128 {
            return Err("cyclic C++ generic type".into());
        }
        let ty = self.get(r, "type")?;
        let keys = match self.class(&ty)? {
            "LimeList" | "LimeSet" => vec!["elementType"],
            "LimeMap" => vec!["keyType", "valueType"],
            _ => vec![],
        };
        let mut children = vec![];
        for k in keys {
            let child = self.get(&ty, k)?;
            self.refs_children(&child, out, active)?;
            children.push(child);
        }
        out.extend(children);
        active.remove(&key);
        Ok(())
    }
    fn types(
        &self,
        v: &Value,
        out: &mut Vec<Value>,
        seen: &mut BTreeSet<String>,
    ) -> Result<(), String> {
        if !seen.insert(v.to_string()) || seen.len() > 128 {
            return Err("cyclic or duplicate nested type".into());
        }
        let kind = self.class(v)?;
        out.push(v.clone());
        if matches!(kind, "LimeStruct" | "LimeClass" | "LimeInterface") {
            for k in [
                "structs",
                "enumerations",
                "exceptions",
                "typeAliases",
                "classes",
                "interfaces",
                "lambdas",
            ] {
                for child in self.array(v, k)? {
                    self.types(&child, out, seen)?;
                }
            }
        }
        Ok(())
    }
    fn function_refs(&self, v: &Value, out: &mut Vec<Value>) -> Result<(), String> {
        for p in self.array(v, "parameters")? {
            out.push(self.get(&p, "typeRef")?);
        }
        out.push(self.get(&self.get(v, "returnType")?, "typeRef")?);
        Ok(())
    }
    fn refs(&self, types: &[Value]) -> Result<Vec<Value>, String> {
        let mut out = vec![];
        for t in types {
            match self.class(t)? {
                "LimeStruct" | "LimeClass" | "LimeInterface" => {
                    for c in self.array(t, "constants")? {
                        out.push(self.get(&c, "typeRef")?);
                    }
                    if self.class(t)? == "LimeStruct" {
                        for f in self.array(t, "fields")? {
                            out.push(self.get(&f, "typeRef")?);
                        }
                    }
                    for f in self.array(t, "functions")? {
                        self.function_refs(&f, &mut out)?;
                    }
                    if self.class(t)? != "LimeStruct" {
                        for p in self.array(t, "properties")? {
                            out.push(self.get(&p, "typeRef")?);
                        }
                    }
                }
                "LimeTypeAlias" => out.push(self.get(t, "typeRef")?),
                "LimeLambda" => self.function_refs(t, &mut out)?,
                "LimeEnumeration" => (),
                "LimeException" => out.push(self.get(t, "errorType")?),
                other => return Err(format!("unsupported native C++ type {other}")),
            }
        }
        let initial = out.clone();
        for r in initial {
            self.refs_children(&r, &mut out, &mut BTreeSet::new())?;
        }
        Ok(out)
    }
    fn ref_includes(
        &self,
        r: &Value,
        out: &mut BTreeSet<Include>,
        active: &mut BTreeSet<String>,
    ) -> Result<(), String> {
        let key = r.to_string();
        if !active.insert(key.clone()) || active.len() > 128 {
            return Err("cyclic C++ include type".into());
        }
        let ty = self.get(r, "type")?;
        self.type_includes(&ty, out, active)?;
        if self.attrs(r)?.contains_key("OPTIMIZED") {
            out.insert(Self::system("memory"));
        }
        let actual = self.actual(&ty)?;
        if matches!(self.class(&actual)?, "LimeClass" | "LimeInterface") {
            out.insert(Self::system("memory"));
        } else if self
            .get(r, "isNullable")?
            .as_bool()
            .ok_or("invalid nullability")?
        {
            out.insert(self.internal("Optional.h"));
        }
        active.remove(&key);
        Ok(())
    }
    fn type_includes(
        &self,
        t: &Value,
        out: &mut BTreeSet<Include>,
        active: &mut BTreeSet<String>,
    ) -> Result<(), String> {
        match self.class(t)? {
            "LimeBasicType" => {
                let id = self.get(t, "typeId")?;
                if id.get("enum").and_then(Value::as_str)
                    != Some("com.here.gluecodium.model.lime.LimeBasicType$TypeId")
                {
                    return Err("invalid basic type ID".into());
                }
                match id
                    .get("name")
                    .and_then(Value::as_str)
                    .ok_or("invalid basic type ID")?
                {
                    "INT8" | "UINT8" | "INT16" | "UINT16" | "INT32" | "UINT32" | "INT64"
                    | "UINT64" => {
                        out.insert(Self::system("cstdint"));
                    }
                    "STRING" => {
                        out.insert(Self::system("string"));
                    }
                    "DATE" => {
                        out.insert(Self::system("chrono"));
                        out.insert(self.internal("TimePointHash.h"));
                    }
                    "DURATION" => {
                        out.insert(Self::system("chrono"));
                        out.insert(self.internal("DurationHash.h"));
                    }
                    "LOCALE" => {
                        out.insert(self.internal("Locale.h"));
                    }
                    "BLOB" => {
                        for x in ["memory", "vector", "cstdint"] {
                            out.insert(Self::system(x));
                        }
                    }
                    "VOID" | "BOOLEAN" | "FLOAT" | "DOUBLE" => (),
                    x => return Err(format!("unsupported basic type {x}")),
                }
            }
            "LimeList" | "LimeSet" | "LimeMap" => {
                let kind = self.class(t)?;
                let k = if kind == "LimeMap" {
                    "keyType"
                } else {
                    "elementType"
                };
                let first = self.get(t, k)?;
                self.ref_includes(&first, out, active)?;
                if kind == "LimeMap" {
                    self.ref_includes(&self.get(t, "valueType")?, out, active)?;
                }
                if kind != "LimeList" {
                    let a = self.actual(&self.get(&first, "type")?)?;
                    if !matches!(
                        self.class(&a)?,
                        "LimeBasicType" | "LimeList" | "LimeSet" | "LimeMap"
                    ) {
                        out.insert(self.internal("Hash.h"));
                    }
                }
                let (system, internal) = match kind {
                    "LimeList" => ("vector", "VectorHash.h"),
                    "LimeSet" => ("unordered_set", "UnorderedSetHash.h"),
                    _ => ("unordered_map", "UnorderedMapHash.h"),
                };
                out.insert(Self::system(system));
                out.insert(self.internal(internal));
            }
            "LimeLambda" => {
                out.insert(self.inc(t)?);
                out.insert(Self::system("functional"));
            }
            "LimeStruct" | "LimeClass" | "LimeInterface" | "LimeEnumeration" | "LimeTypeAlias"
            | "LimeException" => {
                out.insert(self.inc(t)?);
            }
            other => return Err(format!("unsupported native C++ include type {other}")),
        }
        Ok(())
    }
    fn values(
        &self,
        v: &Value,
        out: &mut BTreeSet<Include>,
        active: &mut BTreeSet<String>,
    ) -> Result<(), String> {
        let key = v.to_string();
        if !active.insert(key.clone()) || active.len() > 128 {
            return Err("cyclic C++ value".into());
        }
        match self.class(v)? {
            "LimeValue$Literal" | "LimeValue$Null" => (),
            "LimeValue$Special" => {
                out.insert(Self::system("limits"));
            }
            "LimeValue$Constant" => {
                let c = self.get(&self.get(v, "valueRef")?, "element")?;
                out.insert(self.inc(&c)?);
            }
            "LimeValue$KeyValuePair" => {
                self.values(&self.get(v, "key")?, out, active)?;
                self.values(&self.get(v, "value")?, out, active)?;
            }
            "LimeValue$InitializerList" | "LimeValue$StructInitializer" => {
                if self.class(v)? == "LimeValue$StructInitializer" {
                    self.ref_includes(&self.get(v, "typeRef")?, out, &mut BTreeSet::new())?;
                }
                for x in self.array(v, "values")? {
                    self.values(&x, out, active)?;
                }
            }
            x => return Err(format!("unsupported native C++ value {x}")),
        }
        active.remove(&key);
        Ok(())
    }
    fn collect_values(&self, t: &Value, out: &mut BTreeSet<Include>) -> Result<(), String> {
        match self.class(t)? {
            "LimeClass" | "LimeInterface" | "LimeStruct" => {
                for c in self.array(t, "constants")? {
                    self.values(&self.get(&c, "value")?, out, &mut BTreeSet::new())?;
                }
                if self.class(t)? == "LimeStruct" {
                    for f in self.array(t, "fields")? {
                        let v = self.get(&f, "defaultValue")?;
                        if !v.is_null() {
                            self.values(&v, out, &mut BTreeSet::new())?;
                        }
                    }
                } else {
                    for k in ["structs", "classes", "interfaces"] {
                        for child in self.array(t, k)? {
                            self.collect_values(&child, out)?;
                        }
                    }
                }
            }
            _ => (),
        }
        Ok(())
    }
}

pub(super) fn collect(c: &Context<'_>, root: &Value) -> Result<Collected, String> {
    let mut types = vec![];
    c.types(root, &mut types, &mut BTreeSet::new())?;
    let refs = c.refs(&types)?;
    let mut nesting = BTreeSet::new();
    let mut candidates = vec![];
    for r in &refs {
        let t = c.get(r, "type")?;
        let kind = c.class(&t)?;
        if matches!(
            kind,
            "LimeClass"
                | "LimeInterface"
                | "LimeEnumeration"
                | "LimeStruct"
                | "LimeTypeAlias"
                | "LimeLambda"
        ) {
            let p = c.path(&t)?;
            if p.tail.len() > 1 {
                nesting.insert(p.parent());
            }
            if matches!(kind, "LimeClass" | "LimeInterface") && p.tail.len() == 1 {
                candidates.push((p, t));
            }
        }
    }
    let root_path = c.path(root)?;
    candidates.retain(|(p, _)| *p != root_path && !nesting.contains(p));
    candidates.sort_by_key(|(p, _)| p.text());
    candidates.dedup_by(|a, b| a.0 == b.0);
    let mut header = BTreeSet::new();
    let mut implementation = BTreeSet::new();
    for r in &refs {
        c.ref_includes(r, &mut header, &mut BTreeSet::new())?;
        let t = c.get(r, "type")?;
        if matches!(c.class(&t)?, "LimeClass" | "LimeInterface") && c.path(&t)?.tail.len() == 1 {
            implementation.insert(c.inc(&t)?);
        }
    }
    for t in &types {
        c.type_includes(t, &mut header, &mut BTreeSet::new())?;
        match c.class(t)? {
            "LimeEnumeration" => {
                header.insert(Context::system("cstdint"));
            }
            "LimeStruct" => {
                implementation.insert(Context::system("utility"));
            }
            "LimeInterface" => {
                header.insert(c.internal("TypeRepository.h"));
            }
            "LimeClass" if c.get(t, "isOpen")?.as_bool().ok_or("invalid isOpen")? => {
                header.insert(c.internal("TypeRepository.h"));
            }
            _ => (),
        }
    }
    c.collect_values(root, &mut header)?;
    for (_, t) in &candidates {
        let mut removed = BTreeSet::new();
        c.type_includes(t, &mut removed, &mut BTreeSet::new())?;
        for x in removed {
            header.remove(&x);
        }
    }
    fn groups(
        c: &Context<'_>,
        items: &[(ModelPath, Value)],
        level: usize,
    ) -> Result<Vec<Value>, String> {
        let mut result = vec![];
        let mut i = 0;
        while i < items.len() {
            if items[i].0.head.len() <= level {
                i += 1;
                continue;
            }
            let name = &items[i].0.head[level];
            let mut end = i + 1;
            while end < items.len() && items[end].0.head.get(level) == Some(name) {
                end += 1;
            }
            let subset = &items[i..end];
            let mut types = vec![];
            for (p, v) in subset {
                if p.head.len() == level + 1 {
                    types.push(c.name(v)?);
                }
            }
            let subs = groups(c, subset, level + 1)?;
            result.push(json!({"namespace":name,"types":types,"subGroups":subs}));
            i = end;
        }
        Ok(result)
    }
    Ok(Collected {
        header_includes: header.into_iter().collect(),
        implementation_includes: implementation.into_iter().collect(),
        forward_declarations: Value::Array(groups(c, &candidates, 0)?),
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn dependency_includes_match_jvm_snapshots() {
        for fixture in ["default", "custom"] {
            let base = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
                .join("tests/cpp-generation-goldens")
                .join(fixture);
            let job: Value =
                serde_json::from_slice(&std::fs::read(base.join("job.json")).unwrap()).unwrap();
            let graph = Graph::import_with_absences(
                job.get("snapshot"),
                job.get("property_overlays"),
                job.get("absent_properties"),
            )
            .unwrap();
            let options = &job["options"];
            let config = NativeCppConfig {
                root_namespace: options["root_namespace"]
                    .as_array()
                    .map(|a| a.iter().map(|v| v.as_str().unwrap().to_owned()).collect())
                    .unwrap_or_default(),
                internal_namespace: options["internal_namespace"]
                    .as_array()
                    .map(|a| a.iter().map(|v| v.as_str().unwrap().to_owned()).collect())
                    .unwrap_or_default(),
                ..Default::default()
            };
            let c = Context::new(&graph, &config).unwrap();
            for root in c
                .array(graph.root.as_ref().unwrap(), "topElements")
                .unwrap()
            {
                let path = c.output(&root).unwrap();
                let result = collect(&c, &root).unwrap();
                let expected = |kind: &str| -> Option<Vec<Include>> {
                    let (dir, ext) = if kind == "header" {
                        ("include", "h")
                    } else {
                        ("src", "cpp")
                    };
                    let contents =
                        std::fs::read_to_string(base.join(format!("files/cpp/{dir}/{path}.{ext}")))
                            .ok()?;
                    let mut includes = Vec::new();
                    for line in contents.lines().filter_map(|s| s.strip_prefix("#include ")) {
                        let is_system = line.starts_with('<');
                        let file_name = line.trim_matches(&['<', '>', '\"'][..]).to_owned();
                        if file_name == format!("{path}.h")
                            || file_name.rsplit('/').next().unwrap().starts_with("Export")
                        {
                            continue;
                        }
                        includes.push(Include {
                            file_name,
                            is_system,
                        });
                    }
                    Some(includes)
                };
                if fixture == "custom"
                    && (path.ends_with("/RenamedService") || path.ends_with("/Data"))
                {
                    assert_eq!(
                        result.forward_declarations,
                        json!([{
                            "namespace": "oracle", "types": [], "subGroups": [{
                                "namespace": "custom", "types": ["Worker"], "subGroups": []
                            }]
                        }])
                    );
                }
                let mut header = result.header_includes;
                header.retain(|i| i.file_name != format!("{path}.h"));
                assert_eq!(
                    header,
                    expected("header").unwrap(),
                    "{fixture}: {path} header"
                );
                if let Some(impl_expected) = expected("impl") {
                    let mut actual = result.implementation_includes;
                    actual.retain(|i| i.file_name != format!("{path}.h"));
                    assert_eq!(actual, impl_expected, "{fixture}: {path} implementation");
                }
            }
        }
    }
}
