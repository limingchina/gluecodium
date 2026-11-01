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
            ("predicate exact".into(), 853),
            (
                "predicate error: native controls nonempty comment content unsupported".into(),
                4
            ),
            ("sort exact".into(), 12),
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
    for name in ["m9-class", "m9-struct"] {
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
