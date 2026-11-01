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

fn rename_package(job: &mut Value, old: [&str; 2], new: [&str; 2]) {
    let root = job["snapshot"]["root"]["$ref"].as_str().unwrap().to_owned();
    for node in nodes(job) {
        if node["class"].as_str().unwrap().ends_with(".LimePath")
            && node["properties"]["head"] == json!(old)
        {
            node["properties"]["head"] = json!(new);
        }
    }
    let old_prefix = format!("{}.{}.", old[0], old[1]);
    let new_prefix = format!("{}.{}.", new[0], new[1]);
    for map in ["referenceMap", "fileNameMap"] {
        let map = node_mut(job, &root)["properties"][map]
            .as_object_mut()
            .unwrap();
        let entries = std::mem::take(map);
        for (key, value) in entries {
            let key = key
                .strip_prefix(&old_prefix)
                .map(|suffix| format!("{new_prefix}{suffix}"))
                .unwrap_or(key);
            assert!(map.insert(key, value).is_none());
        }
    }
}

#[test]
fn raw_package_paths_control_file_ownership_includes_and_namespaces() {
    let mut job = fixture("default");
    let original_overlays = job["property_overlays"].clone();
    rename_package(&mut job, ["oracle", "basic"], ["changed", "api"]);
    assert_eq!(job["property_overlays"], original_overlays);
    let generated = generate(TEMPLATES, &job).unwrap();
    assert!(generated
        .iter()
        .any(|f| f.path == Path::new("cpp/include/changed/api/Shade.h")));
    assert!(generated
        .iter()
        .any(|f| f.path == Path::new("cpp/src/changed/api/Data.cpp")));
    assert!(!generated
        .iter()
        .any(|f| f.path.to_string_lossy().contains("oracle/basic/")));
    let callback = generated
        .iter()
        .find(|f| f.path.ends_with("changed/api/Callback.h"))
        .unwrap();
    assert!(callback
        .contents
        .contains("#include \"changed/api/Shade.h\""));
    assert!(callback.contents.contains("::changed::api::Shade"));
    let data = generated
        .iter()
        .find(|f| f.path.ends_with("changed/api/Data.cpp"))
        .unwrap();
    assert!(data.contents.contains("#include \"changed/api/Data.h\""));
    assert!(generated
        .iter()
        .all(|f| !f.contents.contains("oracle::basic")));
    assert!(generated
        .iter()
        .all(|f| !f.contents.contains("namespace oracle {")));

    let mut job = fixture("custom");
    rename_package(&mut job, ["oracle", "custom"], ["changed", "api"]);
    let generated = generate(TEMPLATES, &job).unwrap();
    let data = generated
        .iter()
        .find(|f| f.path.ends_with("acme/api/changed/api/Data.h"))
        .unwrap();
    assert!(data
        .contents
        .contains("#include \"acme/api/changed/api/RenamedService.h\""));
    assert!(data.contents.contains("namespace changed {"));
    assert!(data.contents.contains("class Worker;"));
    assert!(data.contents.contains("::acme::api::changed::api::Worker"));
    assert!(!data.contents.contains("oracle::custom"));
    assert!(!data.contents.contains("namespace oracle {"));
}

#[test]
fn raw_declaration_order_changes_bytes_and_preserves_dependency_sorting() {
    let mut job = fixture("default");
    let original_overlays = job["property_overlays"].clone();
    let baseline = generate(TEMPLATES, &job).unwrap();
    let shade = node_id(&job, "LimeEnumeration", "Shade");
    node_mut(&mut job, &shade)["properties"]["enumerators"]
        .as_array_mut()
        .unwrap()
        .reverse();
    assert_eq!(job["property_overlays"], original_overlays);
    let changed = generate(TEMPLATES, &job).unwrap();
    let file = |files: Vec<GeneratedFile>, suffix: &str| {
        files
            .into_iter()
            .find(|f| f.path.ends_with(suffix))
            .unwrap()
            .contents
    };
    let before = file(baseline.clone(), "oracle/basic/Shade.h");
    let after = file(changed.clone(), "oracle/basic/Shade.h");
    assert!(before.find("RED,").unwrap() < before.find("BLUE = 7").unwrap());
    assert!(after.find("BLUE = 7,").unwrap() < after.find("RED").unwrap());
    assert_ne!(before, after);
    let data_before = file(baseline, "oracle/basic/Data.h");
    let data_after = file(changed, "oracle/basic/Data.h");
    assert_eq!(data_before, data_after);
    assert!(
        data_after.find("using EarlierAlias").unwrap()
            < data_after.find("using LaterAlias").unwrap()
    );
}

fn raw_comment_job() -> Value {
    let mut job = fixture("default");
    job["version"] = json!(2);
    let ids: Vec<String> = job["snapshot"]["nodes"]
        .as_array()
        .unwrap()
        .iter()
        .filter(|n| n["class"].as_str().unwrap().ends_with(".LimeComment"))
        .map(|n| n["id"].as_str().unwrap().to_string())
        .collect();
    let mut raw = serde_json::Map::new();
    for id in ids {
        raw.insert(id.clone(), json!([]));
        if let Some(fields) = job["property_overlays"][&id].as_object_mut() {
            fields.remove("isEmpty");
        }
    }
    job["raw_comments"] = raw.into();
    job
}
fn comment_id(job: &mut Value, kind: &str, name: &str) -> String {
    let id = node_id(job, kind, name);
    node_mut(job, &id)["properties"]["comment"]["$ref"]
        .as_str()
        .unwrap()
        .into()
}
fn data_header(job: &Value) -> String {
    generate(TEMPLATES, job)
        .unwrap()
        .into_iter()
        .find(|f| f.path.ends_with("oracle/basic/Data.h"))
        .unwrap()
        .contents
}
#[test]
fn version_two_comments_are_computed_from_raw_facts() {
    let mut job = raw_comment_job();
    let id = comment_id(&mut job, "LimeStruct", "Data");
    let base = data_header(&job);
    job["raw_comments"][&id] = json!([
        ["", "Hello "],
        ["Java", "ignored"],
        ["Cpp", "world."],
        ["", "\n\nNext paragraph."]
    ]);
    let documented = data_header(&job);
    assert!(
        documented.contains(" * Hello world.\n *\n * Next paragraph."),
        "{documented}"
    );
    assert_ne!(documented, base);
    job["raw_comments"][&id] = json!([["Java", "nonempty elsewhere"]]);
    assert_eq!(data_header(&job), base);
    job["raw_comments"][&id] = json!([["Cpp", "Changed text."]]);
    assert!(data_header(&job).contains(" * Changed text."));
    node_mut(&mut job, &id)["properties"]["isExcluded"] = json!(true);
    assert!(data_header(&job).contains(" * \\private"));
    job["raw_comments"][&id] = json!([["", "  \t "]]);
    let excluded = data_header(&job);
    assert!(excluded.contains(" * \\private"));
    assert!(!excluded.contains("Changed text."));
}
#[test]
fn version_two_rejects_invalid_raw_comments_and_unsupported_syntax() {
    let base = raw_comment_job();
    let mut cases = Vec::new();
    let mut job = base.clone();
    let id = comment_id(&mut job, "LimeStruct", "Data");
    job["raw_comments"].as_object_mut().unwrap().remove(&id);
    cases.push(job);
    let mut job = base.clone();
    job["raw_comments"]["unknown"] = json!([]);
    cases.push(job);
    let mut job = base.clone();
    job["raw_comments"][&id] = json!([["Cpp"]]);
    cases.push(job);
    let mut job = base.clone();
    job["raw_comments"][&id] = json!([["Cpp", 4]]);
    cases.push(job);
    let mut job = base.clone();
    job["property_overlays"][&id]["isEmpty"] = json!(true);
    cases.push(job);
    let mut job = base.clone();
    job["raw_comments"][&id] = json!([["Placeholder", "missing"]]);
    cases.push(job);
    let mut job = base.clone();
    node_mut(&mut job, &id)["properties"]["placeholders"] = json!({"self":{"$ref":id}});
    cases.push(job);
    let mut job = base.clone();
    job["raw_comments"][&id] = json!([["", "See [Other]."]]);
    cases.push(job);
    let mut job = base.clone();
    job["raw_comments"][&id] = json!([["", "**bold**"]]);
    cases.push(job);
    let mut job = base.clone();
    let alias = node_id(&job, "LimeTypeAlias", "Labels");
    let alias_comment = comment_id(&mut job, "LimeTypeAlias", "Labels");
    let root = job["snapshot"]["root"]["$ref"].as_str().unwrap().to_owned();
    node_mut(&mut job, &root)["properties"]["topElements"]
        .as_array_mut()
        .unwrap()
        .retain(|item| item["$ref"] != alias);
    node_mut(&mut job, &root)["properties"]["auxiliaryElements"]
        .as_array_mut()
        .unwrap()
        .push(json!({"$ref":alias}));
    job["raw_comments"][&alias_comment] = json!([["Cpp", "[unsupported auxiliary link]"]]);
    cases.push(job);
    let mut job = base.clone();
    job["version"] = json!(1);
    cases.push(job);
    let mut job = base.clone();
    job.as_object_mut().unwrap().remove("raw_comments");
    cases.push(job);
    let mut job = fixture("default");
    job["raw_comments"] = Value::Null;
    cases.push(job);
    let mut job = base.clone();
    job["raw_comments"] = Value::Null;
    cases.push(job);
    let mut job = base.clone();
    node_mut(&mut job, &id)["properties"]["isEmpty"] = json!(true);
    cases.push(job);
    let mut job = base.clone();
    node_mut(&mut job, &id)["properties"]["selectedText"] = json!("forged");
    cases.push(job);
    let mut job = base.clone();
    let owner = node_id(&job, "LimeStruct", "Data");
    node_mut(&mut job, &id)["properties"]["placeholders"] = json!({"bad": {"$ref":owner}});
    cases.push(job);
    for job in cases {
        assert!(generate(TEMPLATES, &job).is_err());
    }
    let mut ignored = base;
    ignored["raw_comments"][&id] = json!([["Java", "[not cpp] **bold**"]]);
    assert!(generate(TEMPLATES, &ignored).is_ok());
}

#[test]
fn version_two_resolves_placeholder_mutations_and_rejects_cycles() {
    let mut job = raw_comment_job();
    let owner = comment_id(&mut job, "LimeStruct", "Data");
    let target = comment_id(&mut job, "LimeField", "count");
    node_mut(&mut job, &owner)["properties"]["placeholders"] = json!({"part": {"$ref": target}});
    job["raw_comments"][&owner] =
        json!([["", "Prefix "], ["Placeholder", "part"], ["", " suffix."]]);
    job["raw_comments"][&target] = json!([["", " first "], ["Java", "ignored"], ["Cpp", "word "]]);
    assert!(data_header(&job).contains(" * Prefix first word suffix."));
    job["raw_comments"][&target] = json!([["Cpp", " second "]]);
    assert!(data_header(&job).contains(" * Prefix second suffix."));
    job["raw_comments"][&target] = json!([]);
    assert!(data_header(&job).contains(" * Prefix  suffix."));
    node_mut(&mut job, &target)["properties"]["placeholders"] = json!({"back": {"$ref": owner}});
    assert!(generate(TEMPLATES, &job).is_err());
}

#[test]
fn invalid_late_raw_documentation_preserves_existing_output() {
    let dir = tmp("comment-preflight");
    let _ = fs::remove_dir_all(&dir);
    fs::create_dir_all(dir.join("out/cpp/include")).unwrap();
    fs::write(dir.join("out/cpp/include/existing.h"), b"preserve this").unwrap();
    let mut job = raw_comment_job();
    let id = comment_id(&mut job, "LimeTypeAlias", "Labels");
    job["raw_comments"][&id] = json!([["Cpp", "Invalid [reference]."]]);
    let path = dir.join("job.json");
    fs::write(&path, serde_json::to_vec(&job).unwrap()).unwrap();
    let result = Command::new(env!("CARGO_BIN_EXE_ruscodium"))
        .args(["generate-cpp", "--job"])
        .arg(&path)
        .args(["--templates", TEMPLATES, "--output"])
        .arg(dir.join("out"))
        .output()
        .unwrap();
    assert!(!result.status.success());
    assert!(result.stdout.is_empty());
    assert_eq!(
        fs::read(dir.join("out/cpp/include/existing.h")).unwrap(),
        b"preserve this"
    );
    fs::remove_dir_all(dir).unwrap();
}

#[test]
fn documentation_file_sets_match_jvm_bytes_and_source_sets() {
    for case in ["docs", "comments-file-interface", "comments-file-lambda"] {
        let root = Path::new("tests/cpp-documentation-goldens").join(case);
        let job: Value = serde_json::from_slice(&fs::read(root.join("job.json")).unwrap()).unwrap();
        let manifest: Value =
            serde_json::from_slice(&fs::read(root.join("manifest.json")).unwrap()).unwrap();
        let expected = manifest["files"].as_object().unwrap();
        let generated = generate(TEMPLATES, &job).unwrap();
        assert_eq!(generated.len(), expected.len(), "{case}");
        for file in generated {
            let path = file.path.to_str().unwrap();
            let source_set = match file.source_set {
                SourceSet::MAIN => "MAIN",
                SourceSet::COMMON => "COMMON",
            };
            assert_eq!(expected[path], source_set, "{case}/{path}");
            assert_eq!(
                file.contents.as_bytes(),
                fs::read(root.join("files").join(path)).unwrap(),
                "{case}/{path}"
            );
        }
    }
}

#[test]
fn empty_placeholder_dag_does_not_expand_exponentially() {
    let mut job = raw_comment_job();
    let ids: Vec<String> = job["raw_comments"]
        .as_object()
        .unwrap()
        .keys()
        .take(40)
        .cloned()
        .collect();
    for pair in ids.windows(2) {
        node_mut(&mut job, &pair[0])["properties"]["placeholders"] =
            json!({"next":{"$ref":pair[1]}});
        job["raw_comments"][&pair[0]] = json!([["Placeholder", "next"], ["Placeholder", "next"]]);
    }
    assert!(generate(TEMPLATES, &job).is_ok());
}

#[test]
fn documentation_generation_is_deterministic_without_jvm_on_path() {
    let root = Path::new("tests/cpp-documentation-goldens/docs");
    let manifest: Value =
        serde_json::from_slice(&fs::read(root.join("manifest.json")).unwrap()).unwrap();
    let dir = tmp("comment-no-jvm");
    let _ = fs::remove_dir_all(&dir);
    fs::create_dir_all(&dir).unwrap();
    for name in ["first", "second"] {
        let output = Command::new(env!("CARGO_BIN_EXE_ruscodium"))
            .args(["generate-cpp", "--job"])
            .arg(root.join("job.json"))
            .args(["--templates", TEMPLATES, "--output"])
            .arg(dir.join(name))
            .env("PATH", "")
            .output()
            .unwrap();
        assert!(
            output.status.success(),
            "{}",
            String::from_utf8_lossy(&output.stderr)
        );
        assert!(output.stdout.is_empty());
    }
    for path in manifest["files"].as_object().unwrap().keys() {
        let expected = fs::read(root.join("files").join(path)).unwrap();
        assert_eq!(fs::read(dir.join("first").join(path)).unwrap(), expected);
        assert_eq!(fs::read(dir.join("second").join(path)).unwrap(), expected);
    }
    fs::remove_dir_all(dir).unwrap();
}
