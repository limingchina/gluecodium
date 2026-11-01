use ruscodium::cpp_generation::{generate, write_files, GeneratedFile, SourceSet};
use serde_json::{json, Value};
use std::{
    collections::{BTreeMap, BTreeSet},
    fs,
    path::{Path, PathBuf},
    process::Command,
};

const TEMPLATES: &str = "../gluecodium/src/main/resources/templates";
fn fixture(name: &str) -> Value {
    serde_json::from_slice(
        &fs::read(format!("tests/cpp-generation-goldens/{name}/job.json")).unwrap(),
    )
    .unwrap()
}
fn files(name: &str) -> Vec<GeneratedFile> {
    generate(TEMPLATES, &fixture(name)).unwrap()
}
fn tmp(name: &str) -> PathBuf {
    std::env::temp_dir().join(format!("ruscodium-cpp-{name}-{}", std::process::id()))
}
fn nodes(job: &mut Value) -> &mut Vec<Value> {
    job["snapshot"]["nodes"].as_array_mut().unwrap()
}
fn node_id(job: &Value, class: &str, path_tail: &str) -> String {
    let nodes = job["snapshot"]["nodes"].as_array().unwrap();
    nodes
        .iter()
        .find(|n| {
            n["class"].as_str().unwrap().ends_with(class)
                && n["properties"]["path"]["$ref"]
                    .as_str()
                    .and_then(|id| nodes.iter().find(|p| p["id"] == id))
                    .is_some_and(|p| {
                        p["properties"]["tail"]
                            .as_array()
                            .is_some_and(|a| a.last().and_then(Value::as_str) == Some(path_tail))
                    })
        })
        .unwrap()["id"]
        .as_str()
        .unwrap()
        .into()
}
fn node_mut<'a>(job: &'a mut Value, id: &str) -> &'a mut Value {
    nodes(job).iter_mut().find(|n| n["id"] == id).unwrap()
}
#[test]
fn complete_file_sets_match_jvm_bytes_and_sources() {
    for name in ["default", "custom"] {
        let generated = files(name);
        let manifest: Value = serde_json::from_slice(
            &fs::read(format!("tests/cpp-generation-goldens/{name}/manifest.json")).unwrap(),
        )
        .unwrap();
        let expected = manifest["files"].as_object().unwrap();
        let mut seen = BTreeSet::new();
        for f in &generated {
            let path = f.path.to_str().unwrap();
            assert!(seen.insert(path.to_string()));
            let expected_set = match f.source_set {
                SourceSet::MAIN => "MAIN",
                SourceSet::COMMON => "COMMON",
            };
            assert_eq!(expected[path], expected_set, "{name}/{path}");
            assert_eq!(
                f.contents.as_bytes(),
                fs::read(
                    Path::new("tests/cpp-generation-goldens")
                        .join(name)
                        .join("files")
                        .join(path)
                )
                .unwrap(),
                "{name}/{path}"
            );
        }
        assert_eq!(seen.len(), expected.len());
        assert_eq!(
            generated
                .iter()
                .filter(|f| f.source_set == SourceSet::COMMON)
                .count(),
            17
        );
        assert_eq!(generated.len(), if name == "default" { 26 } else { 24 });
    }
}
#[test]
fn output_and_dependencies_follow_raw_model_mutations() {
    let mut job = fixture("default");
    let field_id = node_id(&job, "LimeField", "count");
    let reference = node_mut(&mut job, &field_id)["properties"]["typeRef"]["$ref"]
        .as_str()
        .unwrap()
        .to_owned();
    let string_ref = job["snapshot"]["nodes"]
        .as_array()
        .unwrap()
        .iter()
        .find(|n| {
            n["class"].as_str().unwrap().ends_with("LimeBasicTypeRef")
                && n["properties"]["type"]["$ref"].as_str().is_some_and(|id| {
                    let all = job["snapshot"]["nodes"].as_array().unwrap();
                    all.iter()
                        .find(|n| n["id"] == id)
                        .is_some_and(|n| n["properties"]["typeId"]["name"] == "STRING")
                })
        })
        .cloned()
        .unwrap();
    let original = generate(TEMPLATES, &job).unwrap();
    node_mut(&mut job, &reference)["properties"]["type"] = string_ref["properties"]["type"].clone();
    node_mut(&mut job, &reference)["properties"]["element"] =
        string_ref["properties"]["type"].clone();
    node_mut(&mut job, &reference)["properties"]["elementFullName"] = json!("STRING");
    let changed = generate(TEMPLATES, &job).unwrap();
    let header = |files: Vec<GeneratedFile>| {
        files
            .into_iter()
            .find(|f| f.path.ends_with("oracle/basic/Data.h"))
            .unwrap()
            .contents
    };
    assert_ne!(header(original), header(changed));
    let mut custom = fixture("custom");
    let id = node_id(&custom, "LimeClass", "Service");
    let attr = node_mut(&mut custom, &id)["properties"]["attributes"]["$ref"]
        .as_str()
        .unwrap()
        .to_owned();
    node_mut(&mut custom, &attr)["properties"]["attributes"]["CPP"]["NAME"] =
        json!("ChangedService");
    let generated = generate(TEMPLATES, &custom).unwrap();
    assert!(generated
        .iter()
        .any(|f| f.path.ends_with("ChangedService.h")));
    assert!(generated
        .iter()
        .any(|f| f.contents.contains("ChangedService.h")));

    let mut custom = fixture("custom");
    let original = generate(TEMPLATES, &custom).unwrap();
    let id = node_id(&custom, "LimeField", "worker");
    let reference = node_mut(&mut custom, &id)["properties"]["typeRef"]["$ref"]
        .as_str()
        .unwrap()
        .to_owned();
    let model = custom["snapshot"]["root"]["$ref"]
        .as_str()
        .unwrap()
        .to_owned();
    let int_type = node_mut(&mut custom, &model)["properties"]["referenceMap"]["Int"].clone();
    node_mut(&mut custom, &reference)["properties"]["type"] = int_type.clone();
    node_mut(&mut custom, &reference)["properties"]["element"] = int_type;
    let changed = generate(TEMPLATES, &custom).unwrap();
    let contents = |files: Vec<GeneratedFile>| {
        files
            .into_iter()
            .find(|f| f.path.ends_with("oracle/custom/Data.h"))
            .unwrap()
            .contents
    };
    let before = contents(original);
    let after = contents(changed);
    assert!(before.contains("class Worker;"));
    assert!(!after.contains("class Worker;"));
    assert!(after.contains("Optional.h"));
}
#[test]
fn invalid_jobs_are_rejected_before_output_and_stdout() {
    let base = fixture("default");
    let dir = tmp("invalid");
    let _ = fs::remove_dir_all(&dir);
    fs::create_dir_all(&dir).unwrap();
    fs::write(dir.join("sentinel"), b"keep").unwrap();
    fs::create_dir_all(dir.join("out/cpp/include")).unwrap();
    fs::write(dir.join("out/cpp/include/previous.h"), b"previous").unwrap();
    let mut cases = Vec::new();
    for key in ["data", "template", "hooks", "includes", "headerContext"] {
        let mut j = base.clone();
        j[key] = json!({});
        cases.push(j);
    }
    let mut j = base.clone();
    j["options"]["unknown"] = json!(true);
    cases.push(j);
    let mut j = base.clone();
    j["options"]["root_namespace"] = json!(["../escape"]);
    cases.push(j);
    let mut j = base.clone();
    j["snapshot"]["root"] = j["snapshot"]["nodes"][0]["properties"]["topElements"][0].clone();
    cases.push(j);
    let mut j = base.clone();
    let id = node_id(&j, "LimeStruct", "Data");
    j["property_overlays"][&id]["includes"] = json!([]);
    cases.push(j);
    let mut j = base.clone();
    let id = node_id(&j, "LimeStruct", "Data");
    node_mut(&mut j, &id)["properties"]["headerContext"] = json!({});
    cases.push(j);
    let mut j = base.clone();
    let id = node_id(&j, "LimeInterface", "Worker");
    node_mut(&mut j, &id)["properties"]["parents"] = json!([{}]);
    cases.push(j);
    let model_id = base["snapshot"]["root"]["$ref"]
        .as_str()
        .unwrap()
        .to_owned();
    let mut j = base.clone();
    node_mut(&mut j, &model_id)["properties"]["referenceMap"]
        .as_object_mut()
        .unwrap()
        .remove("oracle.basic.Data.label");
    cases.push(j);
    let mut j = base.clone();
    let string = node_mut(&mut j, &model_id)["properties"]["referenceMap"]["String"].clone();
    node_mut(&mut j, &model_id)["properties"]["referenceMap"]["Int"] = string;
    cases.push(j);
    let mut j = base.clone();
    nodes(&mut j).push(json!({"id":"evil","class":"com.here.gluecodium.model.lime.LimeUnsupported","properties":{}}));
    cases.push(j);
    let mut j = base.clone();
    let comment = nodes(&mut j)
        .iter()
        .find(|n| n["class"].as_str().unwrap().ends_with("LimeComment"))
        .unwrap()["id"]
        .as_str()
        .unwrap()
        .to_owned();
    node_mut(&mut j, &comment)["properties"]["placeholders"] = json!({"0":"hidden"});
    cases.push(j);
    let mut j = base.clone();
    let id = node_id(&j, "LimeStruct", "Data");
    node_mut(&mut j, &id)["properties"]["exportName"] = json!("FORGED");
    cases.push(j);
    let mut j = base.clone();
    let id = node_id(&j, "LimeStruct", "Data");
    j["property_overlays"][&id]["actualType"] = json!(42);
    cases.push(j);
    let mut j = base.clone();
    let id = node_id(&j, "LimeStruct", "Data");
    let attr = node_mut(&mut j, &id)["properties"]["attributes"]["$ref"]
        .as_str()
        .unwrap()
        .to_owned();
    node_mut(&mut j, &attr)["properties"]["attributes"] =
        json!({"CPP":{"NAME":"ExportGluecodiumCpp"}});
    j["options"]["internal_namespace"] = json!(["oracle", "basic"]);
    cases.push(j);
    let mut j = base.clone();
    let owner = node_id(&j, "LimeStruct", "Data");
    let removed = node_id(&j, "LimeField", "count");
    node_mut(&mut j, &owner)["properties"]["fields"]
        .as_array_mut()
        .unwrap()
        .retain(|v| v["$ref"] != removed);
    cases.push(j);
    let mut j = base.clone();
    let owner = node_id(&j, "LimeInterface", "Worker");
    let removed = node_id(&j, "LimeFunction", "run");
    node_mut(&mut j, &owner)["properties"]["functions"]
        .as_array_mut()
        .unwrap()
        .retain(|v| v["$ref"] != removed);
    cases.push(j);
    let mut j = base.clone();
    let id = node_id(&j, "LimeFunction", "run");
    node_mut(&mut j, &id)["properties"]["isStatic"] = json!("false");
    cases.push(j);
    let mut j = base.clone();
    let id = node_id(&j, "LimeInterface", "Worker");
    node_mut(&mut j, &id)["properties"]["isOpen"] = json!(5);
    cases.push(j);
    let mut j = base.clone();
    let id = node_id(&j, "LimeStruct", "Data");
    node_mut(&mut j, &id)["properties"]["childTypes"] = json!(42);
    cases.push(j);
    let mut j = base.clone();
    let id = node_id(&j, "LimeStruct", "Data");
    node_mut(&mut j, &id)["properties"]["childTypes"] = json!([]);
    cases.push(j);
    let mut j = base.clone();
    let id = nodes(&mut j)
        .iter()
        .find(|n| n["class"].as_str().unwrap().ends_with("LimeComment"))
        .unwrap()["id"]
        .as_str()
        .unwrap()
        .to_owned();
    node_mut(&mut j, &id)["properties"]["path"] = json!({"$ref":id});
    cases.push(j);
    let mut j = base.clone();
    let id = nodes(&mut j)
        .iter()
        .find(|n| n["class"].as_str().unwrap().ends_with("LimeBasicTypeRef"))
        .unwrap()["id"]
        .as_str()
        .unwrap()
        .to_owned();
    let other = node_id(&j, "LimeInterface", "Worker");
    node_mut(&mut j, &id)["properties"]["element"] = json!({"$ref":other});
    cases.push(j);
    let mut j = base.clone();
    let id = node_id(&j, "LimeInterface", "Worker");
    let methods = node_mut(&mut j, &id)["properties"]["functions"]
        .as_array_mut()
        .unwrap();
    methods.push(methods[0].clone());
    cases.push(j);
    let mut j = base.clone();
    let id = nodes(&mut j)
        .iter()
        .find(|n| n["class"].as_str().unwrap().ends_with("LimeComment"))
        .unwrap()["id"]
        .as_str()
        .unwrap()
        .to_owned();
    node_mut(&mut j, &id)["properties"]["path"] =
        json!({"enum":"com.here.gluecodium.model.lime.LimePath","name":"forged"});
    cases.push(j);
    let mut j = fixture("custom");
    let id = node_id(&j, "LimeField", "value");
    let type_ref = node_mut(&mut j, &id)["properties"]["typeRef"]["$ref"]
        .as_str()
        .unwrap()
        .to_owned();
    let attributes = node_mut(&mut j, &id)["properties"]["attributes"].clone();
    let model = j["snapshot"]["root"]["$ref"].as_str().unwrap().to_owned();
    let date = node_mut(&mut j, &model)["properties"]["referenceMap"]["Date"].clone();
    node_mut(&mut j, &type_ref)["properties"]["type"] = date.clone();
    node_mut(&mut j, &type_ref)["properties"]["element"] = date;
    node_mut(&mut j, &type_ref)["properties"]["elementFullName"] = json!("DATE");
    node_mut(&mut j, &id)["properties"]["defaultValue"] = json!({"$ref":"unsupported-date"});
    nodes(&mut j).push(json!({"id":"unsupported-date","class":"com.here.gluecodium.model.lime.LimeValue$Literal","properties":{"attributes":attributes,"typeRef":{"$ref":type_ref},"value":"7"}}));
    cases.push(j);
    let mut j = base.clone();
    let alias = node_id(&j, "LimeTypeAlias", "Labels");
    let model = j["snapshot"]["root"]["$ref"].as_str().unwrap().to_owned();
    node_mut(&mut j, &model)["properties"]["topElements"]
        .as_array_mut()
        .unwrap()
        .retain(|v| v["$ref"] != alias);
    node_mut(&mut j, &model)["properties"]["auxiliaryElements"]
        .as_array_mut()
        .unwrap()
        .push(json!({"$ref":alias}));
    let reference = node_mut(&mut j, &alias)["properties"]["typeRef"]["$ref"]
        .as_str()
        .unwrap()
        .to_owned();
    node_mut(&mut j, &reference)["properties"]["type"] = json!({"$ref":alias});
    node_mut(&mut j, &reference)["properties"]["element"] = json!({"$ref":alias});
    cases.push(j);
    for (i, job) in cases.iter().enumerate() {
        assert!(generate(TEMPLATES, job).is_err(), "case {i}");
        let path = dir.join("job.json");
        fs::write(&path, serde_json::to_vec(job).unwrap()).unwrap();
        let out = Command::new(env!("CARGO_BIN_EXE_ruscodium"))
            .args(["generate-cpp", "--job"])
            .arg(&path)
            .args(["--templates", TEMPLATES, "--output"])
            .arg(dir.join("out"))
            .output()
            .unwrap();
        assert!(!out.status.success(), "case {i}");
        assert!(out.stdout.is_empty());
        assert_eq!(
            fs::read(dir.join("out/cpp/include/previous.h")).unwrap(),
            b"previous"
        );
        assert_eq!(fs::read(dir.join("sentinel")).unwrap(), b"keep");
    }
    let incomplete_templates = dir.join("templates");
    fs::create_dir_all(&incomplete_templates).unwrap();
    let path = dir.join("valid-job.json");
    fs::write(&path, serde_json::to_vec(&base).unwrap()).unwrap();
    let result = Command::new(env!("CARGO_BIN_EXE_ruscodium"))
        .args(["generate-cpp", "--job"])
        .arg(path)
        .arg("--templates")
        .arg(incomplete_templates)
        .arg("--output")
        .arg(dir.join("out"))
        .output()
        .unwrap();
    assert!(!result.status.success());
    assert!(result.stdout.is_empty());
    assert_eq!(
        fs::read(dir.join("out/cpp/include/previous.h")).unwrap(),
        b"previous"
    );
    fs::remove_dir_all(dir).unwrap();
}
#[test]
fn output_paths_and_symlinks_are_preflighted() {
    let dir = tmp("write");
    let _ = fs::remove_dir_all(&dir);
    fs::create_dir_all(&dir).unwrap();
    let invalid = GeneratedFile {
        path: "../escape".into(),
        source_set: SourceSet::MAIN,
        contents: "bad".into(),
    };
    assert!(write_files(&dir, &[invalid]).is_err());
    let f = GeneratedFile {
        path: "x/y.h".into(),
        source_set: SourceSet::MAIN,
        contents: "ok".into(),
    };
    assert!(write_files(&dir, &[f.clone(), f.clone()]).is_err());
    #[cfg(unix)]
    {
        std::os::unix::fs::symlink("/tmp", dir.join("x")).unwrap();
        assert!(write_files(&dir, &[f]).is_err());
    }
    fs::remove_dir_all(dir).unwrap();
}
#[test]
fn deterministic_inventory() {
    let one = files("default");
    let two = files("default");
    let index = |files: Vec<GeneratedFile>| {
        files
            .into_iter()
            .map(|f| (f.path, (f.source_set, f.contents)))
            .collect::<BTreeMap<_, _>>()
    };
    assert_eq!(index(one), index(two));
}

#[test]
fn dependencies_reorder_nested_aliases_in_the_complete_header() {
    let mut job = fixture("default");
    let data = node_id(&job, "LimeStruct", "Data");
    let later = node_id(&job, "LimeTypeAlias", "LaterAlias");
    let earlier = node_id(&job, "LimeTypeAlias", "EarlierAlias");
    let aliases = node_mut(&mut job, &data)["properties"]["typeAliases"]
        .as_array()
        .unwrap();
    assert_eq!(aliases[0]["$ref"], later);
    assert_eq!(aliases[1]["$ref"], earlier);
    let header = generate(TEMPLATES, &job)
        .unwrap()
        .into_iter()
        .find(|f| f.path.ends_with("oracle/basic/Data.h"))
        .unwrap()
        .contents;
    assert!(header.find("using EarlierAlias").unwrap() < header.find("using LaterAlias").unwrap());
    assert!(header.contains("#include <unordered_set>"));
}
