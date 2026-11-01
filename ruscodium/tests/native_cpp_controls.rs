use ruscodium::template::{
    native_controls::{predicate, sort},
    Graph,
};
use serde_json::Value;
use std::{collections::BTreeMap, fs};

#[test]
fn inventory_recorded_controls() {
    let mut files = fs::read_dir("tests/template-goldens")
        .unwrap()
        .map(|x| x.unwrap().path())
        .filter(|p| p.to_string_lossy().ends_with(".request.json"))
        .collect::<Vec<_>>();
    files.sort();
    let mut counts = BTreeMap::<String, usize>::new();
    let mut unsupported = Vec::new();
    for path in files {
        let request: Value = serde_json::from_slice(&fs::read(&path).unwrap()).unwrap();
        let graph = Graph::import_with_absences(
            request.get("snapshot"),
            request.get("property_overlays"),
            request.get("absent_properties"),
        )
        .unwrap();
        for cell in request["hooks"]["predicates"]
            .as_array()
            .into_iter()
            .flatten()
        {
            let name = cell["name"].as_str().unwrap();
            match predicate(&graph, name, &cell["receiver"]) {
                Ok(result) => {
                    assert_eq!(
                        Some(result),
                        cell["result"].as_bool(),
                        "{} {cell}",
                        path.display()
                    );
                    *counts.entry("predicate exact".into()).or_default() += 1;
                }
                Err(e) => {
                    unsupported.push((
                        path.file_name().unwrap().to_string_lossy().to_string(),
                        cell["receiver"]["$ref"].as_str().unwrap().to_string(),
                    ));
                    assert_eq!(
                        e,
                        "native controls nonempty comment content unsupported",
                        "{} {cell}",
                        path.display()
                    );
                    *counts.entry(format!("predicate error: {e}")).or_default() += 1;
                }
            }
        }
        for cell in request["hooks"]["sorters"].as_array().into_iter().flatten() {
            let name = cell["name"].as_str().unwrap();
            match sort(&graph, name, cell["input"].as_array().unwrap()) {
                Ok(result) => {
                    assert_eq!(
                        Value::Array(result),
                        cell["result"],
                        "{} {cell}",
                        path.display()
                    );
                    *counts.entry("sort exact".into()).or_default() += 1;
                }
                Err(e) => panic!("unexpected sorter error in {}: {cell}: {e}", path.display()),
            }
        }
    }
    assert_eq!(
        counts,
        BTreeMap::from([
            ("predicate exact".into(), 1095),
            (
                "predicate error: native controls nonempty comment content unsupported".into(),
                4
            ),
            ("sort exact".into(), 15),
        ])
    );
    assert_eq!(
        unsupported,
        vec![
            ("cpp-enumeration.request.json".into(), "n1".into()),
            ("cpp-enumeration.request.json".into(), "n3".into()),
            ("cpp-function.request.json".into(), "n1".into()),
            ("model-helpers.request.json".into(), "n2".into()),
        ]
    );
}

fn matrix() -> Value {
    serde_json::from_slice(&fs::read("tests/template-goldens/native-matrix.request.json").unwrap())
        .unwrap()
}
fn graph(req: &Value) -> Graph {
    Graph::import_with_absences(
        req.get("snapshot"),
        req.get("property_overlays"),
        req.get("absent_properties"),
    )
    .unwrap()
}
fn node_mut<'a>(req: &'a mut Value, id: &str) -> &'a mut Value {
    req["snapshot"]["nodes"]
        .as_array_mut()
        .unwrap()
        .iter_mut()
        .find(|n| n["id"] == id)
        .unwrap()
}
#[test]
fn raw_facts_drive_predicates_and_sorting() {
    let mut req = matrix();
    let g = graph(&req);
    let field = serde_json::json!({"$ref":"n25"});
    let tr = serde_json::json!({"$ref":"n75"});
    assert!(predicate(&g, "needsRefSuffix", &tr).unwrap());
    assert!(predicate(&g, "needsPointerValueEqual", &field).unwrap());
    assert!(predicate(&g, "needsRawPointerEqual", &field).unwrap());
    node_mut(&mut req, "n75")["properties"]["isNullable"] = false.into();
    let g = graph(&req);
    assert!(!predicate(&g, "needsRawPointerEqual", &field).unwrap());
    assert!(!predicate(&g, "needsPointerValueEqual", &field).unwrap());
    assert!(predicate(&g, "needsNotNullComment", &tr).unwrap());
    let data = serde_json::json!({"$ref":"n49"});
    let alias = serde_json::json!({"$ref":"n43"});
    let target = serde_json::json!({"$ref":"n50"});
    let input = vec![
        data.clone(),
        alias.clone(),
        target.clone(),
        Value::String("ignored".into()),
    ];
    let result = sort(&g, "", &input).unwrap();
    assert_eq!(result, vec![target, alias, data]);
    assert_eq!(sort(&g, "", &result).unwrap(), result);
    assert!(sort(&g, "", &[field.clone(), field])
        .unwrap_err()
        .contains("duplicate"));
    assert!(sort(&g, "unknown", &[]).is_err());
    assert!(predicate(&g, "unknown", &Value::Null).is_err());
}
#[test]
fn config_and_empty_selection_guards() {
    use ruscodium::template::{native_cpp::NativeCppConfig, render};
    for value in [
        serde_json::json!({"predicates":null}),
        serde_json::json!({"sorters":"yes"}),
    ] {
        assert!(NativeCppConfig::parse(&value).is_err());
    }
    let mut req = matrix();
    req["native_cpp"] = serde_json::json!({"predicates":true,"sorters":true});
    assert!(render("../gluecodium/src/main/resources/templates", &req)
        .unwrap_err()
        .contains("name hooks"));
    req["hooks"]["names"] = serde_json::json!([]);
    req["hooks"]["predicates"] =
        serde_json::json!([{"name":"hasAnyComment", "receiver": null, "result": false}]);
    assert!(render("../gluecodium/src/main/resources/templates", &req)
        .unwrap_err()
        .contains("predicates hooks"));
    req["hooks"]["predicates"] = serde_json::json!([]);
    req["hooks"]["registered_predicates"] = serde_json::json!(["hasAnyComment"]);
    assert!(render("../gluecodium/src/main/resources/templates", &req)
        .unwrap_err()
        .contains("registered_predicates"));
    req["hooks"]["registered_predicates"] = serde_json::json!([]);
    req["hooks"]["sorters"] = serde_json::json!([{"name":"","input":[],"result":[]}]);
    assert!(render("../gluecodium/src/main/resources/templates", &req)
        .unwrap_err()
        .contains("sorters hooks"));
}

#[test]
fn unchanged_fragments_render_with_all_native_controls() {
    for name in [
        "m9-class",
        "m9-struct",
        "m9-field-defaults",
        "m9-field-frozen",
        "m9-field-accessors",
    ] {
        let mut req: Value = serde_json::from_slice(
            &fs::read(format!("tests/template-goldens/{name}.request.json")).unwrap(),
        )
        .unwrap();
        req["native_cpp"] = serde_json::json!({"predicates":true,"sorters":true});
        req["hooks"] = serde_json::json!({});
        let actual =
            ruscodium::template::render("../gluecodium/src/main/resources/templates", &req)
                .unwrap();
        let expected =
            fs::read_to_string(format!("tests/template-goldens/{name}.expected")).unwrap();
        assert_eq!(actual, expected, "{name}");
    }
}

#[test]
fn malformed_cycles_and_missing_required_facts_fail() {
    let mut req = matrix();
    node_mut(&mut req, "n238")["properties"]["type"] = serde_json::json!({"$ref":"n43"});
    let g = graph(&req);
    assert!(
        predicate(&g, "needsRefSuffix", &serde_json::json!({"$ref":"n238"}))
            .unwrap_err()
            .contains("cyclic alias")
    );
    node_mut(&mut req, "n230")["properties"]["type"] = serde_json::json!({"$ref":"n43"});
    node_mut(&mut req, "n238")["properties"]["type"] = serde_json::json!({"$ref":"n41"});
    let g = graph(&req);
    assert!(sort(
        &g,
        "",
        &[
            serde_json::json!({"$ref":"n41"}),
            serde_json::json!({"$ref":"n43"})
        ]
    )
    .unwrap_err()
    .contains("Cycle detected"));
    let mut req = matrix();
    node_mut(&mut req, "n75")["properties"]
        .as_object_mut()
        .unwrap()
        .remove("isNullable");
    assert!(predicate(
        &graph(&req),
        "needsRefSuffix",
        &serde_json::json!({"$ref":"n75"})
    )
    .unwrap_err()
    .contains("missing isNullable"));
}

#[test]
fn selectors_on_empty_input_and_failures_preserve_outputs() {
    let path =
        std::env::temp_dir().join(format!("ruscodium-native-controls-{}", std::process::id()));
    fs::create_dir_all(&path).unwrap();
    let mut req = serde_json::json!({"schema":"gluecodium.template.render-request","version":1,"template":"test","data":{"items":[]},"native_cpp":{"predicates":true,"sorters":true}});
    fs::write(
        path.join("test.mustache"),
        "{{#filter items predicate=\"needsRefSuffix\"}}yes{{/filter}}",
    )
    .unwrap();
    assert_eq!(ruscodium::template::render(&path, &req).unwrap(), "yes");
    fs::write(
        path.join("test.mustache"),
        "before{{#filter items predicate=\"unknown\"}}yes{{/filter}}",
    )
    .unwrap();
    assert!(ruscodium::template::render(&path, &req)
        .unwrap_err()
        .contains("predicate"));
    fs::write(
        path.join("test.mustache"),
        "before{{#sort items sorter=\"unknown\"}}yes{{/sort}}",
    )
    .unwrap();
    assert!(ruscodium::template::render(&path, &req)
        .unwrap_err()
        .contains("sorter"));
    let request = path.join("request.json");
    let output = path.join("out");
    fs::write(&request, serde_json::to_vec(&req).unwrap()).unwrap();
    fs::write(&output, "sentinel").unwrap();
    for args in [vec!["--output", output.to_str().unwrap()], vec![]] {
        let result = std::process::Command::new(env!("CARGO_BIN_EXE_ruscodium"))
            .args(["render", "--templates"])
            .arg(&path)
            .arg("--request")
            .arg(&request)
            .args(args)
            .output()
            .unwrap();
        assert!(!result.status.success());
        assert!(result.stdout.is_empty());
        assert_eq!(fs::read_to_string(&output).unwrap(), "sentinel");
    }
    req["native_cpp"]["sorters"] = false.into();
    assert!(ruscodium::template::render(&path, &req)
        .unwrap_err()
        .contains("replay"));
    fs::remove_dir_all(path).unwrap();
}

#[test]
fn exclusions_apply_only_to_the_owning_comment() {
    let mut req = matrix();
    let fun = serde_json::json!({"$ref":"n270"});
    node_mut(&mut req, "n343")["properties"]["isExcluded"] = true.into();
    assert!(!predicate(&graph(&req), "hasAnyComment", &fun).unwrap());
    node_mut(&mut req, "n428")["properties"]["isExcluded"] = true.into();
    assert!(predicate(&graph(&req), "hasAnyComment", &fun).unwrap());
}

#[test]
fn malformed_receiver_types_and_struct_members_fail() {
    let mut req = matrix();
    let g = graph(&req);
    assert!(predicate(&g, "needsRefSuffix", &serde_json::json!({"$ref":"missing"})).is_err());
    for malformed in [
        serde_json::json!({"$ref": 123}),
        serde_json::json!({"$ref":"n49", "extra":true}),
    ] {
        assert!(predicate(&g, "needsRefSuffix", &malformed).is_err());
        assert!(sort(&g, "", &[malformed]).is_err());
    }
    assert!(!predicate(&g, "needsRefSuffix", &serde_json::json!({"$ref":"n49"})).unwrap());
    node_mut(&mut req, "n75")["properties"]["type"] = serde_json::json!({"$ref":"n343"});
    node_mut(&mut req, "n75")["properties"]["isNullable"] = false.into();
    assert!(predicate(
        &graph(&req),
        "needsRefSuffix",
        &serde_json::json!({"$ref":"n75"})
    )
    .unwrap_err()
    .contains("invalid type class"));
    let mut malformed_inner = matrix();
    node_mut(&mut malformed_inner, "n44")["properties"]["classes"] =
        serde_json::json!([{"$ref":"n49"}]);
    assert!(predicate(
        &graph(&malformed_inner),
        "needsInnerForwardDeclarations",
        &serde_json::json!({"$ref":"n44"})
    )
    .unwrap_err()
    .contains("invalid classes"));
    let mut req = matrix();
    node_mut(&mut req, "n49")["properties"]["fields"] = serde_json::json!([{"$ref":"n49"}]);
    assert!(sort(&graph(&req), "", &[serde_json::json!({"$ref":"n49"})])
        .unwrap_err()
        .contains("invalid struct fields"));
    node_mut(&mut req, "n49")["class"] = "com.here.gluecodium.model.lime.LimeForged".into();
    assert!(predicate(
        &graph(&req),
        "needsRefSuffix",
        &serde_json::json!({"$ref":"n49"})
    )
    .unwrap_err()
    .contains("unsupported"));
}

#[test]
fn positional_references_and_provable_comment_results() {
    let mut req = matrix();
    node_mut(&mut req, "n75")["class"] =
        "com.here.gluecodium.model.lime.LimePositionalTypeRef".into();
    node_mut(&mut req, "n75")["properties"]["isNullable"] = false.into();
    let g = graph(&req);
    let tr = serde_json::json!({"$ref":"n75"});
    assert!(predicate(&g, "needsRefSuffix", &tr).unwrap());
    assert!(predicate(&g, "needsNotNullComment", &tr).unwrap());
    req["property_overlays"]["n428"]["isEmpty"] = false.into();
    node_mut(&mut req, "n427")["properties"]["attributes"]["DEPRECATED"] = serde_json::json!({});
    assert!(predicate(
        &graph(&req),
        "hasAnyComment",
        &serde_json::json!({"$ref":"n270"})
    )
    .unwrap());
}

#[test]
fn sorting_uses_raw_generic_children() {
    let mut req = matrix();
    node_mut(&mut req, "n393")["properties"]["elementType"] = serde_json::json!({"$ref":"n238"});
    node_mut(&mut req, "n393")["properties"]["childTypes"] = serde_json::json!([]);
    let alias = serde_json::json!({"$ref":"n40"});
    let target = serde_json::json!({"$ref":"n50"});
    assert_eq!(
        sort(&graph(&req), "", &[alias.clone(), target.clone()]).unwrap(),
        vec![target, alias]
    );
}

#[test]
fn malformed_facts_are_not_hidden_by_other_true_conditions() {
    let mut req = matrix();
    node_mut(&mut req, "n427")["properties"]["attributes"]["DEPRECATED"] = serde_json::json!({});
    node_mut(&mut req, "n270")["properties"]
        .as_object_mut()
        .unwrap()
        .remove("returnType");
    assert!(predicate(
        &graph(&req),
        "hasAnyComment",
        &serde_json::json!({"$ref":"n270"})
    )
    .unwrap_err()
    .contains("missing returnType"));
    let mut wrong_kind = matrix();
    node_mut(&mut wrong_kind, "n270")["properties"]["returnType"] =
        serde_json::json!({"$ref":"n49"});
    assert!(predicate(
        &graph(&wrong_kind),
        "hasAnyComment",
        &serde_json::json!({"$ref":"n270"})
    )
    .unwrap_err()
    .contains("invalid return type class"));
    let mut req = matrix();
    node_mut(&mut req, "n239")["properties"]["attributes"]["EQUATABLE"] = Value::Null;
    assert!(predicate(
        &graph(&req),
        "needsPointerValueEqual",
        &serde_json::json!({"$ref":"n6"})
    )
    .unwrap_err()
    .contains("invalid attribute group"));
}

#[test]
fn constructor_predicates_follow_raw_field_defaults() {
    let mut req: Value =
        serde_json::from_slice(&fs::read("tests/template-goldens/m9-matrix.request.json").unwrap())
            .unwrap();
    let root = req["snapshot"]["root"]["$ref"].as_str().unwrap().to_owned();
    let model = node_mut(&mut req, &root);
    let defaults = model["properties"]["referenceMap"]["m9.matrix.Defaults"].clone();
    let first = model["properties"]["referenceMap"]["m9.matrix.Defaults.first"]["$ref"]
        .as_str()
        .unwrap()
        .to_owned();
    assert!(predicate(&graph(&req), "hasPartialDefaults", &defaults).unwrap());
    node_mut(&mut req, &first)["properties"]["defaultValue"] = Value::Null;
    assert!(!predicate(&graph(&req), "hasPartialDefaults", &defaults).unwrap());
    assert!(predicate(&graph(&req), "hasDefaultConstructor", &defaults).unwrap());
}

#[test]
fn common_immutable_traversal_unwraps_generic_field_values() {
    let mut req: Value =
        serde_json::from_slice(&fs::read("tests/template-goldens/m9-matrix.request.json").unwrap())
            .unwrap();
    let root = req["snapshot"]["root"]["$ref"].as_str().unwrap().to_owned();
    let model = node_mut(&mut req, &root);
    let types = model["properties"]["referenceMap"]["m9.matrix.FieldTypes"].clone();
    let types_id = types["$ref"].as_str().unwrap().to_owned();
    let partial_id = model["properties"]["referenceMap"]["m9.matrix.ExplicitPartial"]["$ref"]
        .as_str()
        .unwrap()
        .to_owned();
    let frozen_id = model["properties"]["referenceMap"]["m9.matrix.Frozen"]["$ref"]
        .as_str()
        .unwrap()
        .to_owned();
    let ctor = node_mut(&mut req, &partial_id)["properties"]["fieldConstructors"][0].clone();
    let first_field = node_mut(&mut req, &types_id)["properties"]["fields"][0].clone();
    let ref_id = node_mut(&mut req, ctor["$ref"].as_str().unwrap())["properties"]["fieldRefs"][0]
        ["$ref"]
        .as_str()
        .unwrap()
        .to_owned();
    node_mut(&mut req, &ref_id)["properties"]["element"] = first_field;
    node_mut(&mut req, &types_id)["properties"]["fieldConstructors"] = serde_json::json!([ctor]);
    assert!(predicate(&graph(&req), "needsAllFieldsConstructor", &types).unwrap());
    let attrs_id = node_mut(&mut req, &frozen_id)["properties"]["attributes"]["$ref"]
        .as_str()
        .unwrap()
        .to_owned();
    node_mut(&mut req, &attrs_id)["properties"]["attributes"]
        .as_object_mut()
        .unwrap()
        .remove("IMMUTABLE");
    assert!(!predicate(&graph(&req), "needsAllFieldsConstructor", &types).unwrap());
}

#[test]
fn invalid_constructor_field_references_fail() {
    let mut req: Value =
        serde_json::from_slice(&fs::read("tests/template-goldens/m9-matrix.request.json").unwrap())
            .unwrap();
    let root = req["snapshot"]["root"]["$ref"].as_str().unwrap().to_owned();
    let structure =
        node_mut(&mut req, &root)["properties"]["referenceMap"]["m9.matrix.ExplicitAll"].clone();
    let struct_id = structure["$ref"].as_str().unwrap();
    let comment = node_mut(&mut req, struct_id)["properties"]["comment"].clone();
    let ctor = node_mut(&mut req, struct_id)["properties"]["fieldConstructors"][0]["$ref"]
        .as_str()
        .unwrap()
        .to_owned();
    node_mut(&mut req, &ctor)["properties"]["fieldRefs"][0] = comment;
    assert!(
        predicate(&graph(&req), "needsAllFieldsConstructor", &structure)
            .unwrap_err()
            .contains("invalid field reference class")
    );
}

#[test]
fn jvm_generic_constructor_cases_exercise_distinct_immutable_traversals() {
    let req: Value =
        serde_json::from_slice(&fs::read("tests/template-goldens/m9-matrix.request.json").unwrap())
            .unwrap();
    let root = req["snapshot"]["root"]["$ref"].as_str().unwrap();
    let model = req["snapshot"]["nodes"]
        .as_array()
        .unwrap()
        .iter()
        .find(|n| n["id"] == root)
        .unwrap();
    let graph = graph(&req);
    for (name, all_fields) in [
        ("GenericListCtor", true),
        ("GenericSetCtor", true),
        ("GenericMapCtor", true),
        ("GenericMapKeyCtor", false),
    ] {
        let structure = &model["properties"]["referenceMap"][format!("m9.matrix.{name}")];
        assert!(
            predicate(&graph, "hasDefaultConstructor", structure).unwrap(),
            "{name}"
        );
        assert!(
            !predicate(&graph, "hasPartialDefaults", structure).unwrap(),
            "{name}"
        );
        assert_eq!(
            predicate(&graph, "needsAllFieldsConstructor", structure).unwrap(),
            all_fields,
            "{name}"
        );
        for (selector, expected) in [
            ("hasDefaultConstructor", true),
            ("hasPartialDefaults", false),
            ("needsAllFieldsConstructor", all_fields),
        ] {
            assert!(
                req["hooks"]["predicates"]
                    .as_array()
                    .unwrap()
                    .iter()
                    .any(|cell| cell["receiver"] == *structure
                        && cell["name"] == selector
                        && cell["result"] == expected),
                "missing JVM record {name}/{selector}"
            );
        }
    }
}
