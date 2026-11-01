//! Bounded native C++ predicate and declaration-sort providers.
use super::graph::{reference, Graph};
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};

const PREDICATES: &[&str] = &[
    "needsRefSuffix",
    "needsNotNullComment",
    "hasAnyComment",
    "hasDefaultConstructor",
    "hasPartialDefaults",
    "needsAllFieldsConstructor",
    "needsPointerValueEqual",
    "needsRawPointerEqual",
    "isUsedInAnotherInnerClasses",
    "needsInnerForwardDeclarations",
    "asyncFunNeedsSynchronousVersion",
];

pub fn require_predicate(name: &str) -> Result<(), String> {
    if PREDICATES.contains(&name) {
        Ok(())
    } else {
        Err(format!("unsupported native C++ predicate {name}"))
    }
}
pub fn predicate(graph: &Graph, name: &str, receiver: &Value) -> Result<bool, String> {
    require_predicate(name)?;
    graph.validate(receiver)?;
    let ctx = Context { graph };
    ctx.validate_receiver(receiver)?;
    ctx.predicate(name, receiver)
}
pub fn sort(graph: &Graph, selector: &str, input: &[Value]) -> Result<Vec<Value>, String> {
    if !selector.is_empty() {
        return Err(format!("unsupported native C++ sorter {selector}"));
    }
    let ctx = Context { graph };
    for value in input {
        graph.validate(value)?;
        ctx.validate_receiver(value)?;
    }
    ctx.sort(input)
}
struct Context<'a> {
    graph: &'a Graph,
}
impl<'a> Context<'a> {
    fn validate_receiver(&self, v: &Value) -> Result<(), String> {
        let Some(id) = reference(v) else {
            return Ok(());
        };
        let node = self
            .graph
            .nodes
            .get(id)
            .ok_or_else(|| format!("native controls missing node {id}"))?;
        let class = node
            .class
            .strip_prefix("com.here.gluecodium.model.lime.")
            .ok_or_else(|| format!("unsupported native controls model class {}", node.class))?;
        if matches!(
            class,
            "LimeAmbiguousConstantRef"
                | "LimeAmbiguousTypeRef"
                | "LimeAttributes"
                | "LimeBasicType"
                | "LimeBasicTypeRef"
                | "LimeClass"
                | "LimeComment"
                | "LimeConstant"
                | "LimeDirectTypeRef"
                | "LimeEnumeration"
                | "LimeEnumerator"
                | "LimeException"
                | "LimeExternalDescriptor"
                | "LimeField"
                | "LimeFieldConstructor"
                | "LimeFunction"
                | "LimeInterface"
                | "LimeLambda"
                | "LimeLambdaParameter"
                | "LimeLazyFieldRef"
                | "LimeLazyFunctionCall"
                | "LimeLazyTypeRef"
                | "LimeList"
                | "LimeMap"
                | "LimeModel"
                | "LimeParameter"
                | "LimePath"
                | "LimePositionalEnumeratorRef"
                | "LimePositionalTypeRef"
                | "LimeProperty"
                | "LimeReturnType"
                | "LimeSet"
                | "LimeStruct"
                | "LimeThrownType"
                | "LimeTypeAlias"
                | "LimeValue$Constant"
                | "LimeValue$Literal"
                | "LimeValue$Null"
                | "LimeValue$Special"
                | "LimeValue$InitializerList"
                | "LimeValue$StructInitializer"
                | "LimeValue$KeyValuePair"
                | "LimeValue$Duration"
        ) {
            Ok(())
        } else {
            Err(format!(
                "unsupported native controls model class {}",
                node.class
            ))
        }
    }
    fn class<'b>(&'b self, v: &'b Value) -> &'b str {
        self.graph
            .class(v)
            .and_then(|c| c.strip_prefix("com.here.gluecodium.model.lime."))
            .unwrap_or("")
    }
    fn get(&self, v: &Value, key: &str) -> Result<&'a Value, String> {
        let id = reference(v).ok_or("native controls expected model reference")?;
        let node = self
            .graph
            .nodes
            .get(id)
            .ok_or_else(|| format!("native controls missing node {id}"))?;
        node.properties
            .get(key)
            .ok_or_else(|| format!("native controls missing {key} on {} ({id})", node.class))
    }
    fn list(&self, v: &Value, key: &str) -> Result<&'a Vec<Value>, String> {
        self.get(v, key)?
            .as_array()
            .ok_or_else(|| format!("native controls invalid {key} array"))
    }
    fn boolean(&self, v: &Value, key: &str) -> Result<bool, String> {
        self.get(v, key)?
            .as_bool()
            .ok_or_else(|| format!("native controls invalid {key} boolean"))
    }
    fn attr(&self, v: &Value, group: &str, key: Option<&str>) -> Result<bool, String> {
        let attrs = self
            .get(self.get(v, "attributes")?, "attributes")?
            .as_object()
            .ok_or("invalid attributes")?;
        match (attrs.get(group), key) {
            (Some(x), None) => {
                x.as_object().ok_or("invalid attribute group")?;
                Ok(true)
            }
            (Some(x), Some(k)) => Ok(x
                .as_object()
                .ok_or("invalid attribute group")?
                .get(k)
                .is_some_and(|v| !v.is_null() && v != &Value::Bool(false))),
            _ => Ok(false),
        }
    }
    fn actual(&self, v: &Value) -> Result<Value, String> {
        let mut v = v.clone();
        let mut seen = BTreeSet::new();
        while self.class(&v) == "LimeTypeAlias" {
            let id = reference(&v).ok_or("invalid alias")?;
            if !seen.insert(id.to_owned()) || seen.len() > 128 {
                return Err("native controls cyclic alias dependency".into());
            }
            v = self.raw_type(self.get(&v, "typeRef")?)?.clone();
        }
        if !matches!(
            self.class(&v),
            "LimeBasicType"
                | "LimeEnumeration"
                | "LimeStruct"
                | "LimeClass"
                | "LimeInterface"
                | "LimeLambda"
                | "LimeException"
                | "LimeList"
                | "LimeSet"
                | "LimeMap"
        ) {
            return Err(format!(
                "native controls invalid type class {}",
                self.class(&v)
            ));
        }
        Ok(v)
    }
    fn raw_type<'b>(&self, tr: &'b Value) -> Result<&'a Value, String> {
        if !self.is_ref(tr) {
            return Err("native controls invalid type reference class".into());
        }
        let ty = self.get(tr, "type")?;
        if !matches!(
            self.class(ty),
            "LimeBasicType"
                | "LimeEnumeration"
                | "LimeStruct"
                | "LimeClass"
                | "LimeInterface"
                | "LimeLambda"
                | "LimeException"
                | "LimeList"
                | "LimeSet"
                | "LimeMap"
                | "LimeTypeAlias"
        ) {
            return Err(format!(
                "native controls invalid type class {}",
                self.class(ty)
            ));
        }
        Ok(ty)
    }
    fn type_ref(&self, v: &Value) -> Result<Value, String> {
        self.actual(self.raw_type(v)?)
    }
    fn generic_children(&self, ty: &Value) -> Result<Vec<&'a Value>, String> {
        match self.class(ty) {
            "LimeList" | "LimeSet" => Ok(vec![self.get(ty, "elementType")?]),
            "LimeMap" => Ok(vec![self.get(ty, "keyType")?, self.get(ty, "valueType")?]),
            _ => Err("native controls invalid generic type".into()),
        }
    }
    fn is_ref(&self, v: &Value) -> bool {
        matches!(
            self.class(v),
            "LimeBasicTypeRef"
                | "LimeDirectTypeRef"
                | "LimeAmbiguousTypeRef"
                | "LimeLazyTypeRef"
                | "LimePositionalTypeRef"
        )
    }
    fn is_container(&self, v: &Value) -> bool {
        matches!(self.class(v), "LimeStruct" | "LimeClass" | "LimeInterface")
    }
    fn inheritance(&self, v: &Value) -> bool {
        matches!(self.class(v), "LimeClass" | "LimeInterface")
    }
    fn named(&self, v: &Value) -> bool {
        matches!(
            self.class(v),
            "LimeField"
                | "LimeParameter"
                | "LimeLambdaParameter"
                | "LimeFunction"
                | "LimeFieldConstructor"
                | "LimeConstant"
                | "LimeEnumerator"
                | "LimeEnumeration"
                | "LimeTypeAlias"
                | "LimeStruct"
                | "LimeClass"
                | "LimeInterface"
                | "LimeLambda"
                | "LimeProperty"
                | "LimeException"
                | "LimeBasicType"
                | "LimeList"
                | "LimeMap"
                | "LimeSet"
        )
    }
    fn path(&self, v: &Value) -> Result<(Vec<String>, Vec<String>, String), String> {
        let p = self.get(v, "path")?;
        let parts = |k| -> Result<Vec<String>, String> {
            self.list(p, k)?
                .iter()
                .map(|v| {
                    v.as_str()
                        .map(str::to_owned)
                        .ok_or_else(|| format!("invalid path {k}"))
                })
                .collect()
        };
        Ok((
            parts("head")?,
            parts("tail")?,
            self.get(p, "disambiguator")?
                .as_str()
                .ok_or("invalid path disambiguator")?
                .into(),
        ))
    }
    fn full_name(&self, v: &Value) -> Result<String, String> {
        if self.class(v) == "LimeBasicType" {
            let tag = self
                .get(v, "typeId")?
                .get("name")
                .and_then(Value::as_str)
                .ok_or("invalid basic type")?;
            return Ok(match tag {
                "VOID" => "Void",
                "INT8" => "Byte",
                "UINT8" => "UByte",
                "INT16" => "Short",
                "UINT16" => "UShort",
                "INT32" => "Int",
                "UINT32" => "UInt",
                "INT64" => "Long",
                "UINT64" => "ULong",
                "FLOAT" => "Float",
                "DOUBLE" => "Double",
                "BOOLEAN" => "Boolean",
                "STRING" => "String",
                "BLOB" => "Blob",
                "DATE" => "Date",
                "DURATION" => "Duration",
                "LOCALE" => "Locale",
                _ => return Err("invalid basic type id".into()),
            }
            .into());
        }
        let (h, t, d) = self.path(v)?;
        let mut n = h.into_iter().chain(t).collect::<Vec<_>>().join(".");
        if !d.is_empty() {
            n.push(':');
            n.push_str(&d)
        }
        Ok(n)
    }
    fn parent(&self, v: &Value) -> Result<Option<Value>, String> {
        let (h, mut t, _) = self.path(v)?;
        if t.len() <= 1 {
            return Ok(None);
        }
        t.pop();
        let mut found = None;
        for (id, node) in &self.graph.nodes {
            if !node.properties.contains_key("path") || !node.properties.contains_key("external") {
                continue;
            }
            let candidate = json!({"$ref":id});
            if !self.named(&candidate) {
                continue;
            }
            let (ch, ct, cd) = self.path(&candidate)?;
            if ch == h && ct == t && cd.is_empty() {
                if found.is_some() {
                    return Err("native controls duplicate parent".into());
                }
                found = Some(candidate)
            }
        }
        found
            .map(Some)
            .ok_or_else(|| "native controls missing parent context".into())
    }
    fn not_null(&self, v: &Value) -> Result<bool, String> {
        if self.boolean(v, "isNullable")? {
            return Ok(false);
        }
        Ok(self.inheritance(&self.type_ref(v)?))
    }
    fn ref_suffix(&self, v: &Value) -> Result<bool, String> {
        if self.boolean(v, "isNullable")? {
            return Ok(true);
        }
        let ty = self.type_ref(v)?;
        match self.class(&ty) {
            "LimeEnumeration" => Ok(false),
            "LimeBasicType" => {
                let id = self
                    .get(&ty, "typeId")?
                    .get("name")
                    .and_then(Value::as_str)
                    .ok_or("invalid basic type")?;
                match id {
                    "STRING" => Ok(!self.attr(v, "CPP", Some("TYPE"))?),
                    "BLOB" | "DATE" | "LOCALE" => Ok(true),
                    "VOID" | "INT8" | "UINT8" | "INT16" | "UINT16" | "INT32" | "UINT32"
                    | "INT64" | "UINT64" | "FLOAT" | "DOUBLE" | "BOOLEAN" | "DURATION" => Ok(false),
                    _ => Err("native controls invalid basic type id".into()),
                }
            }
            _ => Ok(true),
        }
    }
    fn comment(&self, v: &Value) -> Result<bool, String> {
        if self.class(v) != "LimeComment" {
            return Err("native controls invalid comment class".into());
        }
        if self.boolean(v, "isExcluded")? {
            return Ok(true);
        }
        self.comment_text(v)
    }
    fn comment_text(&self, v: &Value) -> Result<bool, String> {
        if self.class(v) != "LimeComment" {
            return Err("native controls invalid comment class".into());
        }
        if let Some(text) = super::native_comments::selected(self.graph, v)? {
            Ok(!text.is_empty())
        } else if self.boolean(v, "isEmpty")? {
            Ok(false)
        } else {
            Err("native controls nonempty comment content unsupported".into())
        }
    }
    fn has_comment(&self, v: &Value) -> Result<bool, String> {
        if !self.named(v) {
            return Ok(false);
        }
        let mut uncertain = None;
        let mut is_true = false;
        macro_rules! proven {
            ($expr:expr) => {
                match $expr {
                    Ok(true) => is_true = true,
                    Ok(false) => {}
                    Err(error)
                        if error == "native controls nonempty comment content unsupported" =>
                    {
                        if uncertain.is_none() {
                            uncertain = Some(error);
                        }
                    }
                    Err(error) => return Err(error),
                }
            };
        }
        proven!(self.get(v, "comment").and_then(|c| self.comment(c)));
        if self.class(v) == "LimeFunction" {
            let ret = self.get(v, "returnType")?;
            if self.class(ret) != "LimeReturnType" {
                return Err("native controls invalid return type class".into());
            }
            proven!(self.get(ret, "comment").and_then(|c| self.comment_text(c)));
            proven!(self.get(ret, "typeRef").and_then(|tr| self.not_null(tr)));
            match self.get(v, "thrownType") {
                Ok(thrown) if !thrown.is_null() => {
                    if self.class(thrown) != "LimeThrownType" {
                        return Err("native controls invalid thrown type class".into());
                    }
                    proven!(self
                        .get(thrown, "comment")
                        .and_then(|c| self.comment_text(c)))
                }
                Ok(_) => {}
                Err(e) => return Err(e),
            }
            proven!(self.attr(v, "DEPRECATED", None));
            for p in self.list(v, "parameters")? {
                if self.class(p) != "LimeParameter" {
                    return Err("native controls invalid parameter class".into());
                }
                proven!(self.get(p, "comment").and_then(|c| self.comment_text(c)));
                proven!(self.get(p, "typeRef").and_then(|tr| self.not_null(tr)));
            }
        } else {
            proven!(self.attr(v, "DEPRECATED", None));
            if self.class(v) == "LimeFieldConstructor" {
                proven!(self
                    .get(v, "structRef")
                    .and_then(|r| self.raw_type(r))
                    .and_then(|st| self.get(st, "constructorComment"))
                    .and_then(|c| self.comment_text(c)));
            }
        }
        if is_true {
            Ok(true)
        } else {
            match uncertain {
                Some(e) => Err(e),
                None => Ok(false),
            }
        }
    }
    fn immutable(
        &self,
        ty: &Value,
        unwrap: bool,
        visited: &mut BTreeSet<String>,
        depth: usize,
    ) -> Result<bool, String> {
        if depth > 128 {
            return Err("native controls type depth limit".into());
        }
        let mut ty = self.actual(ty)?;
        let mut chain = BTreeSet::new();
        if unwrap {
            loop {
                let key = match self.class(&ty) {
                    "LimeList" | "LimeSet" => "elementType",
                    "LimeMap" => "valueType",
                    _ => break,
                };
                let id = reference(&ty).ok_or("invalid generic type")?;
                if !chain.insert(id.to_owned()) || chain.len() > 128 {
                    return Err("native controls cyclic generic dependency".into());
                }
                ty = self.actual(self.get(self.get(&ty, key)?, "type")?)?;
            }
        }
        let id = reference(&ty).ok_or("invalid type")?.to_owned();
        if !visited.insert(id) {
            return Ok(false);
        }
        if visited.len() > 10000 {
            return Err("native controls type traversal limit".into());
        }
        if self.class(&ty) == "LimeStruct" {
            for field in self.list(&ty, "fields")? {
                if self.class(field) != "LimeField" {
                    return Err("native controls invalid struct field".into());
                }
                if self.immutable(
                    self.get(self.get(field, "typeRef")?, "type")?,
                    unwrap,
                    visited,
                    depth + 1,
                )? {
                    return Ok(true);
                }
            }
        }
        self.attr(&ty, "IMMUTABLE", None)
    }
    fn struct_pred(&self, name: &str, v: &Value) -> Result<bool, String> {
        let fields = self.list(v, "fields")?;
        let ctors = self.list(v, "fieldConstructors")?;
        for field in fields {
            if self.class(field) != "LimeField" {
                return Err("native controls invalid struct field".into());
            }
        }
        for ctor in ctors {
            if self.class(ctor) != "LimeFieldConstructor" {
                return Err("native controls invalid field constructor".into());
            }
            for field_ref in self.list(ctor, "fieldRefs")? {
                if self.class(field_ref) != "LimeLazyFieldRef" {
                    return Err("native controls invalid field reference class".into());
                }
                let field = self.get(field_ref, "element")?;
                if self.class(field) != "LimeField" || !fields.contains(field) {
                    return Err("native controls field constructor references invalid field".into());
                }
            }
        }
        if name == "needsAllFieldsConstructor" {
            if ctors.is_empty() {
                return Ok(true);
            }
            if self.attr(v, "IMMUTABLE", None)?
                || fields
                    .iter()
                    .map(|f| {
                        self.immutable(
                            self.get(self.get(f, "typeRef")?, "type")?,
                            true,
                            &mut BTreeSet::new(),
                            0,
                        )
                    })
                    .collect::<Result<Vec<_>, String>>()?
                    .contains(&true)
            {
                for c in ctors {
                    if self.list(c, "fieldRefs")?.len() == fields.len() {
                        return Ok(false);
                    }
                }
                return Ok(true);
            }
            return Ok(false);
        }
        let mut uninit = Vec::new();
        for f in fields {
            if self.get(f, "defaultValue")?.is_null() {
                uninit.push(f)
            }
        }
        if name == "hasPartialDefaults" {
            return Ok(!uninit.is_empty() && ctors.is_empty() && uninit.len() < fields.len());
        }
        for c in ctors {
            if self.list(c, "fieldRefs")?.is_empty() {
                return Ok(false);
            }
        }
        if uninit.is_empty() {
            return Ok(true);
        }
        for f in uninit {
            if self.immutable(
                self.get(self.get(f, "typeRef")?, "type")?,
                false,
                &mut BTreeSet::new(),
                0,
            )? {
                return Ok(false);
            }
        }
        Ok(!self.attr(v, "IMMUTABLE", None)?)
    }
    fn predicate(&self, name: &str, v: &Value) -> Result<bool, String> {
        match name {
            "needsRefSuffix" => {
                if self.is_ref(v) {
                    self.ref_suffix(v)
                } else {
                    Ok(false)
                }
            }
            "needsNotNullComment" => {
                if self.is_ref(v) {
                    self.not_null(v)
                } else {
                    Ok(false)
                }
            }
            "hasAnyComment" => self.has_comment(v),
            "hasDefaultConstructor" | "hasPartialDefaults" | "needsAllFieldsConstructor" => {
                if self.class(v) == "LimeStruct" {
                    self.struct_pred(name, v)
                } else {
                    Ok(false)
                }
            }
            "needsPointerValueEqual" | "needsRawPointerEqual" => {
                if self.class(v) != "LimeField" {
                    return Ok(false);
                }
                let tr = self.get(v, "typeRef")?;
                let ty = self.type_ref(tr)?;
                let eq = self.inheritance(&ty) && self.attr(&ty, "EQUATABLE", None)?;
                if name == "needsPointerValueEqual" {
                    Ok(eq || self.boolean(tr, "isNullable")?)
                } else {
                    Ok(self.boolean(tr, "isNullable")? && self.inheritance(&ty) && !eq)
                }
            }
            "asyncFunNeedsSynchronousVersion" => {
                if self.class(v) != "LimeFunction" {
                    return Ok(false);
                }
                let mut chain = vec![v.clone()];
                let mut cur = v.clone();
                while let Some(p) = self.parent(&cur)? {
                    if chain.len() > 128 {
                        return Err("native controls parent depth limit".into());
                    }
                    chain.push(p.clone());
                    cur = p;
                }
                for platform in ["JAVA", "KOTLIN", "SWIFT"] {
                    let mut skipped = false;
                    for el in &chain {
                        if self.attr(el, platform, Some("SKIP"))? {
                            skipped = true;
                            break;
                        }
                    }
                    if !skipped {
                        return Ok(true);
                    }
                }
                Ok(false)
            }
            "needsInnerForwardDeclarations" => {
                if !self.is_container(v) {
                    return Ok(false);
                }
                let children = self.inner(v)?;
                self.sibling_imports(&children, None)
            }
            "isUsedInAnotherInnerClasses" => {
                if !self.is_container(v) {
                    return Ok(false);
                }
                let Some(parent) = self.parent(v)? else {
                    return Ok(false);
                };
                if !self.inheritance(&parent) {
                    return Ok(false);
                }
                let children = self.inner(&parent)?;
                self.sibling_imports(&children, Some(v))
            }
            _ => unreachable!(),
        }
    }
    fn checked_list(&self, v: &Value, key: &str, expected: &str) -> Result<&'a Vec<Value>, String> {
        let values = self.list(v, key)?;
        for value in values {
            if self.class(value) != expected {
                return Err(format!("native controls invalid {key} member"));
            }
        }
        Ok(values)
    }
    fn inner(&self, v: &Value) -> Result<Vec<Value>, String> {
        Ok(self
            .checked_list(v, "interfaces", "LimeInterface")?
            .iter()
            .chain(self.checked_list(v, "classes", "LimeClass")?)
            .cloned()
            .collect())
    }
    fn sibling_imports(&self, children: &[Value], target: Option<&Value>) -> Result<bool, String> {
        let targets: Vec<&Value> = target.map_or_else(|| children.iter().collect(), |v| vec![v]);
        for child in targets {
            let name = self.full_name(child)?;
            for other in children {
                if other == child {
                    continue;
                }
                let mut refs = BTreeSet::new();
                self.collect_imports(other, &mut refs, &mut BTreeSet::new())?;
                if refs.contains(&name) {
                    return Ok(true);
                }
            }
        }
        Ok(false)
    }
    fn collect_imports(
        &self,
        v: &Value,
        out: &mut BTreeSet<String>,
        active: &mut BTreeSet<String>,
    ) -> Result<(), String> {
        let id = reference(v).ok_or("invalid nested type")?.to_owned();
        if !active.insert(id.clone()) || active.len() > 128 {
            return Err("native controls cyclic nested types".into());
        }
        if self.is_container(v) {
            for c in self.checked_list(v, "constants", "LimeConstant")? {
                self.import_ref(self.get(c, "typeRef")?, out, &mut BTreeSet::new())?
            }
            if self.class(v) == "LimeStruct" {
                for f in self.checked_list(v, "fields", "LimeField")? {
                    self.import_ref(self.get(f, "typeRef")?, out, &mut BTreeSet::new())?
                }
            }
            for f in self.checked_list(v, "functions", "LimeFunction")? {
                self.import_function(f, out, true)?
            }
            if self.inheritance(v) {
                for p in self.checked_list(v, "properties", "LimeProperty")? {
                    self.import_ref(self.get(p, "typeRef")?, out, &mut BTreeSet::new())?
                }
            }
            for (k, kind) in [
                ("structs", "LimeStruct"),
                ("enumerations", "LimeEnumeration"),
                ("exceptions", "LimeException"),
                ("typeAliases", "LimeTypeAlias"),
                ("classes", "LimeClass"),
                ("interfaces", "LimeInterface"),
                ("lambdas", "LimeLambda"),
            ] {
                for child in self.checked_list(v, k, kind)? {
                    self.collect_imports(child, out, active)?
                }
            }
        } else {
            match self.class(v) {
                "LimeTypeAlias" => {
                    self.import_ref(self.get(v, "typeRef")?, out, &mut BTreeSet::new())?
                }
                "LimeException" => {
                    self.import_ref(self.get(v, "errorType")?, out, &mut BTreeSet::new())?
                }
                "LimeLambda" => self.import_function(v, out, false)?,
                _ => {}
            }
        }
        active.remove(&id);
        Ok(())
    }
    fn import_ref(
        &self,
        tr: &Value,
        out: &mut BTreeSet<String>,
        active: &mut BTreeSet<String>,
    ) -> Result<(), String> {
        let ty = self.raw_type(tr)?;
        let id = reference(ty).ok_or("invalid type reference")?.to_owned();
        let name = if let Some(name) = self.get(tr, "elementFullName").ok().and_then(Value::as_str)
        {
            name.to_owned()
        } else {
            self.full_name(self.get(tr, "element")?)?
        };
        out.insert(name);
        if matches!(self.class(ty), "LimeList" | "LimeSet" | "LimeMap") {
            if !active.insert(id.clone()) || active.len() > 128 {
                return Err("native controls cyclic generic dependency".into());
            }
            for child in self.generic_children(ty)? {
                self.import_ref(child, out, active)?
            }
            active.remove(&id);
        }
        Ok(())
    }
    fn exception_ref(&self, v: &Value) -> Result<Option<Value>, String> {
        let thrown = self.get(v, "thrownType")?;
        if thrown.is_null() {
            return Ok(None);
        }
        let ty = self.type_ref(self.get(thrown, "typeRef")?)?;
        if self.class(&ty) == "LimeException" {
            Ok(Some(self.get(&ty, "errorType")?.clone()))
        } else {
            Ok(None)
        }
    }
    fn import_function(
        &self,
        v: &Value,
        out: &mut BTreeSet<String>,
        has_exception: bool,
    ) -> Result<(), String> {
        for p in self.list(v, "parameters")? {
            self.import_ref(self.get(p, "typeRef")?, out, &mut BTreeSet::new())?
        }
        self.import_ref(
            self.get(self.get(v, "returnType")?, "typeRef")?,
            out,
            &mut BTreeSet::new(),
        )?;
        if has_exception {
            if let Some(tr) = self.exception_ref(v)? {
                if self.class(&self.type_ref(&tr)?) != "LimeEnumeration" {
                    self.import_ref(&tr, out, &mut BTreeSet::new())?
                }
            }
        }
        Ok(())
    }
    fn sort(&self, input: &[Value]) -> Result<Vec<Value>, String> {
        let values: Vec<_> = input.iter().filter(|v| self.named(v)).cloned().collect();
        let mut names = BTreeSet::new();
        let mut deps = BTreeMap::new();
        for v in &values {
            let name = self.full_name(v)?;
            if !names.insert(name) {
                return Err("native controls duplicate sorter full name".into());
            }
        }
        for v in &values {
            let name = self.full_name(v)?;
            let mut d = BTreeSet::new();
            self.dependencies(v, &names, &mut d, &mut BTreeSet::new())?;
            d.remove(&name);
            deps.insert(name, d);
        }
        let mut result = Vec::new();
        let mut used = BTreeSet::new();
        while result.len() < values.len() {
            let mut found = None;
            for v in &values {
                let name = self.full_name(v)?;
                if !used.contains(&name) && deps[&name].is_empty() {
                    found = Some((name, v.clone()));
                    break;
                }
            }
            let (name, v) = found.ok_or("Cycle detected in C++ elements dependencies.")?;
            used.insert(name.clone());
            result.push(v);
            for d in deps.values_mut() {
                d.remove(&name);
            }
        }
        Ok(result)
    }
    fn type_dependencies(
        &self,
        tr: &Value,
        names: &BTreeSet<String>,
        out: &mut BTreeSet<String>,
        active: &mut BTreeSet<String>,
    ) -> Result<(), String> {
        let ty = self.raw_type(tr)?;
        if matches!(self.class(ty), "LimeList" | "LimeSet" | "LimeMap") {
            let id = reference(ty).ok_or("invalid generic")?.to_owned();
            if !active.insert(id.clone()) || active.len() > 128 {
                return Err("native controls cyclic generic dependency".into());
            }
            for child in self.generic_children(ty)? {
                self.type_dependencies(child, names, out, active)?
            }
            active.remove(&id);
        }
        let name = self.full_name(ty)?;
        if names.contains(&name) {
            out.insert(name);
        }
        Ok(())
    }
    fn dependencies(
        &self,
        v: &Value,
        names: &BTreeSet<String>,
        out: &mut BTreeSet<String>,
        active: &mut BTreeSet<String>,
    ) -> Result<(), String> {
        match self.class(v) {
            "LimeField"
            | "LimeParameter"
            | "LimeLambdaParameter"
            | "LimeConstant"
            | "LimeProperty" => {
                self.type_dependencies(self.get(v, "typeRef")?, names, out, active)?
            }
            "LimeStruct" => {
                for (key, kind) in [
                    ("fields", "LimeField"),
                    ("functions", "LimeFunction"),
                    ("constants", "LimeConstant"),
                ] {
                    for child in self.list(v, key)? {
                        if self.class(child) != kind {
                            return Err(format!("native controls invalid struct {key} member"));
                        }
                        self.dependencies(child, names, out, active)?
                    }
                }
            }
            "LimeTypeAlias" => {
                self.type_dependencies(self.get(v, "typeRef")?, names, out, active)?
            }
            "LimeFunction" | "LimeLambda" => {
                for p in self.list(v, "parameters")? {
                    self.type_dependencies(self.get(p, "typeRef")?, names, out, active)?
                }
                self.type_dependencies(
                    self.get(self.get(v, "returnType")?, "typeRef")?,
                    names,
                    out,
                    active,
                )?;
                if self.class(v) == "LimeFunction" {
                    if let Some(tr) = self.exception_ref(v)? {
                        self.type_dependencies(&tr, names, out, active)?
                    }
                }
            }
            _ => {}
        }
        Ok(())
    }
}
