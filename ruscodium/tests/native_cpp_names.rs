use ruscodium::template::{
    native_cpp::{resolve, NativeCppConfig},
    render, Graph,
};
use serde_json::{json, Value};
use std::{collections::BTreeMap, fs, path::Path};

fn request(name: &str) -> Value {
    serde_json::from_slice(
        &fs::read(format!("tests/template-goldens/{name}.request.json")).unwrap(),
    )
    .unwrap()
}
fn graph(request: &Value) -> Graph {
    Graph::import_with_absences(
        request.get("snapshot"),
        request.get("property_overlays"),
        request.get("absent_properties"),
    )
    .unwrap()
}
fn config(name: &str) -> NativeCppConfig {
    if name == "native-matrix" {
        NativeCppConfig::parse(
            &json!({"root_namespace":["outer","api"],"internal_namespace":["detail","impl"]}),
        )
        .unwrap()
    } else if name.starts_with("native-") {
        NativeCppConfig::default()
    } else {
        NativeCppConfig::parse(&json!({"internal_namespace":["internal"]})).unwrap()
    }
}

#[test]
fn every_recorded_name_cell_is_compared_or_explicitly_unsupported() {
    let mut paths = fs::read_dir("tests/template-goldens")
        .unwrap()
        .map(|e| e.unwrap().path())
        .filter(|p| p.to_string_lossy().ends_with(".request.json"))
        .collect::<Vec<_>>();
    paths.sort();
    let mut supported = 0;
    let mut unsupported = BTreeMap::new();
    let mut matrix = 0;
    let mut m9 = 0;
    for path in paths {
        let name = path
            .file_name()
            .unwrap()
            .to_str()
            .unwrap()
            .strip_suffix(".request.json")
            .unwrap();
        let req = request(name);
        let Some(snapshot) = req.get("snapshot") else {
            continue;
        };
        let _ = snapshot;
        let graph = graph(&req);
        for cell in req["hooks"]["names"].as_array().into_iter().flatten() {
            let selector = cell["resolver"].as_str().unwrap();
            let mode = cell["mode"].as_str().unwrap();
            match resolve(&graph, &config(name), selector, mode, &cell["receiver"]) {
                Ok(actual) => {
                    assert_eq!(
                        actual,
                        cell["result"].as_str().map(str::to_owned),
                        "fixture {name}, cell {cell}"
                    );
                    supported += 1;
                    if name.starts_with("m9-") {
                        m9 += 1;
                    }
                    if name == "native-matrix" {
                        matrix += 1;
                    }
                }
                Err(error) => {
                    let reason = if error.starts_with("native C++ missing parent context") {
                        "missing owner"
                    } else if error == "native C++ nonempty or unavailable comment unsupported" {
                        "comment text"
                    } else if error == "unsupported C++ attribute ATTRIBUTE" {
                        "Cpp Attribute"
                    } else {
                        panic!("unexpected unsupported cell in {name}: {cell}: {error}");
                    };
                    *unsupported.entry(reason).or_insert(0) += 1;
                }
            }
        }
    }
    assert_eq!(matrix, 162);
    assert_eq!(m9, 92);
    assert_eq!(supported, 295);
    assert_eq!(
        unsupported,
        BTreeMap::from([
            ("Cpp Attribute", 2),
            ("comment text", 4),
            ("missing owner", 14)
        ])
    );
}

#[test]
fn unchanged_cpp_partials_render_with_native_names() {
    for name in [
        "native-enumeration",
        "native-alias",
        "native-function",
        "native-return",
    ] {
        let mut req = request(name);
        req["native_cpp"] = json!({});
        req["hooks"]["names"] = json!([]);
        let actual = render(
            Path::new("../gluecodium/src/main/resources/templates"),
            &req,
        )
        .unwrap();
        let expected =
            fs::read_to_string(format!("tests/template-goldens/{name}.expected")).unwrap();
        assert_eq!(actual, expected, "{name}");
    }
}

#[test]
fn rejects_invalid_config_mixed_hooks_and_forged_selectors() {
    for invalid in [
        json!(null),
        json!([]),
        json!({"other":[]}),
        json!({"root_namespace":null}),
        json!({"root_namespace":["bad::name"]}),
        json!({"internal_namespace":[4]}),
    ] {
        assert!(NativeCppConfig::parse(&invalid).is_err(), "{invalid}");
    }
    let mut req = request("native-enumeration");
    req["native_cpp"] = json!({});
    assert!(render("../gluecodium/src/main/resources/templates", &req)
        .unwrap_err()
        .contains("cannot be combined"));
    let graph = graph(&req);
    let receiver = &req["hooks"]["names"][0]["receiver"];
    assert!(resolve(
        &graph,
        &config("native-enumeration"),
        "forged",
        "name",
        receiver
    )
    .unwrap_err()
    .contains("resolver"));
    assert!(resolve(
        &graph,
        &config("native-enumeration"),
        "FQN",
        "ref",
        receiver
    )
    .unwrap_err()
    .contains("ref mode"));
    assert!(resolve(
        &graph,
        &config("native-enumeration"),
        "forged",
        "name",
        &Value::Null
    )
    .is_err());
}

#[test]
fn cycles_and_missing_context_report_errors() {
    let mut req = request("native-matrix");
    let nodes = req["snapshot"]["nodes"].as_array_mut().unwrap();
    let alias = nodes
        .iter()
        .find(|n| n["class"].as_str().unwrap().ends_with("LimeTypeAlias"))
        .unwrap();
    let alias_id = alias["id"].as_str().unwrap().to_owned();
    let type_ref = alias["properties"]["typeRef"]["$ref"]
        .as_str()
        .unwrap()
        .to_owned();
    let node = nodes.iter_mut().find(|n| n["id"] == type_ref).unwrap();
    node["properties"]["type"] = json!({"$ref":alias_id});
    let cyclic_graph = graph(&req);
    assert!(resolve(
        &cyclic_graph,
        &config("native-matrix"),
        "",
        "name",
        &json!({"$ref":type_ref})
    )
    .unwrap_err()
    .contains("cyclic alias"));
    let req = request("cpp-function");
    let graph = graph(&req);
    let cell = req["hooks"]["names"]
        .as_array()
        .unwrap()
        .iter()
        .find(|c| {
            graph
                .class(&c["receiver"])
                .is_some_and(|c| c.ends_with("LimeFunction"))
        })
        .unwrap();
    assert!(resolve(
        &graph,
        &config("cpp-function"),
        "",
        "name",
        &cell["receiver"]
    )
    .unwrap_err()
    .contains("missing parent context"));
}

#[test]
fn native_failures_do_not_write_partial_output() {
    let dir = std::env::temp_dir().join(format!("ruscodium-native-failure-{}", std::process::id()));
    fs::create_dir_all(&dir).unwrap();
    let output = dir.join("output");
    let request_file = dir.join("request.json");
    let mut cases = Vec::new();
    let mut invalid = request("native-enumeration");
    invalid["native_cpp"] = json!({"root_namespace":null});
    cases.push(invalid);
    let mut mixed = request("native-enumeration");
    mixed["native_cpp"] = json!({});
    cases.push(mixed);
    let mut comment = request("cpp-enumeration");
    comment["native_cpp"] = json!({"internal_namespace":["internal"]});
    comment["hooks"]["names"] = json!([]);
    cases.push(comment);
    for req in cases {
        fs::write(&output, "sentinel").unwrap();
        fs::write(&request_file, serde_json::to_vec(&req).unwrap()).unwrap();
        let command = |with_output: bool| {
            let mut cmd = std::process::Command::new(env!("CARGO_BIN_EXE_ruscodium"));
            cmd.args([
                "render",
                "--templates",
                "../gluecodium/src/main/resources/templates",
                "--request",
            ])
            .arg(&request_file);
            if with_output {
                cmd.arg("--output").arg(&output);
            }
            cmd.output().unwrap()
        };
        assert!(!command(true).status.success());
        assert_eq!(fs::read_to_string(&output).unwrap(), "sentinel");
        let stdout = command(false);
        assert!(!stdout.status.success());
        assert!(stdout.stdout.is_empty());
    }
    fs::remove_dir_all(dir).unwrap();
}

#[test]
fn unsupported_or_missing_naming_facts_do_not_succeed() {
    let original = request("native-enumeration");
    let receiver = original["data"].clone();
    let id = receiver["$ref"].as_str().unwrap();
    for case in [
        "missing-external",
        "external",
        "attribute",
        "unsupported-class",
    ] {
        let mut req = original.clone();
        let nodes = req["snapshot"]["nodes"].as_array_mut().unwrap();
        let i = nodes.iter().position(|n| n["id"] == id).unwrap();
        match case {
            "missing-external" => {
                nodes[i]["properties"]
                    .as_object_mut()
                    .unwrap()
                    .remove("external");
            }
            "external" => nodes[i]["properties"]["external"] = json!({}),
            "attribute" => {
                let attr_id = nodes[i]["properties"]["attributes"]["$ref"]
                    .as_str()
                    .unwrap()
                    .to_owned();
                let attr = nodes.iter_mut().find(|n| n["id"] == attr_id).unwrap();
                attr["properties"]["attributes"]["CPP"] = json!({"UNKNOWN":true});
            }
            "unsupported-class" => {
                nodes[i]["class"] = json!("com.here.gluecodium.model.lime.LimeLambdaParameter")
            }
            _ => unreachable!(),
        }
        let graph = graph(&req);
        assert!(
            resolve(&graph, &config("native-enumeration"), "", "name", &receiver).is_err(),
            "case {case}"
        );
    }
}

#[test]
fn false_or_null_accessors_attribute_does_not_enable_field_accessors() {
    let original = request("native-matrix");
    let receiver = original["hooks"]["names"]
        .as_array()
        .unwrap()
        .iter()
        .find(|c| c["mode"] == "getter" && c["result"] == "get_h_t_t_p_server")
        .unwrap()["receiver"]
        .clone();
    for value in [json!(false), Value::Null] {
        let mut req = original.clone();
        let attrs = req["snapshot"]["nodes"]
            .as_array_mut()
            .unwrap()
            .iter_mut()
            .find(|n| n["properties"]["attributes"]["CPP"]["ACCESSORS"] == true)
            .unwrap();
        attrs["properties"]["attributes"]["CPP"]["ACCESSORS"] = value;
        let graph = graph(&req);
        for mode in ["getter", "setter"] {
            assert_eq!(
                resolve(&graph, &config("native-matrix"), "C++", mode, &receiver).unwrap(),
                None
            );
        }
    }
}

#[test]
fn rejects_forged_type_reference_class_and_literal_type_id() {
    let original = request("native-matrix");
    let nodes = original["snapshot"]["nodes"].as_array().unwrap();
    let type_ref = nodes
        .iter()
        .find(|n| {
            n["class"]
                .as_str()
                .unwrap()
                .ends_with("LimeAmbiguousTypeRef")
        })
        .unwrap()["id"]
        .as_str()
        .unwrap()
        .to_owned();
    let mut forged = original.clone();
    let nodes = forged["snapshot"]["nodes"].as_array_mut().unwrap();
    nodes.iter_mut().find(|n| n["id"] == type_ref).unwrap()["class"] =
        json!("review.CustomTypeRef");
    let forged_graph = graph(&forged);
    assert!(resolve(
        &forged_graph,
        &config("native-matrix"),
        "FQN",
        "name",
        &json!({"$ref":type_ref})
    )
    .is_err());
    let mut forged = original.clone();
    let nodes = forged["snapshot"]["nodes"].as_array_mut().unwrap();
    let literal = nodes
        .iter()
        .find(|n| n["class"].as_str().unwrap().ends_with("LimeValue$Literal"))
        .unwrap();
    let literal_id = literal["id"].as_str().unwrap().to_owned();
    let type_ref = literal["properties"]["typeRef"]["$ref"]
        .as_str()
        .unwrap()
        .to_owned();
    let type_id = nodes.iter().find(|n| n["id"] == type_ref).unwrap()["properties"]["type"]["$ref"]
        .as_str()
        .unwrap()
        .to_owned();
    nodes.iter_mut().find(|n| n["id"] == type_id).unwrap()["properties"]["typeId"]["name"] =
        json!("UNSUPPORTED");
    let graph = graph(&forged);
    assert!(resolve(
        &graph,
        &config("native-matrix"),
        "",
        "name",
        &json!({"$ref":literal_id})
    )
    .is_err());
}
