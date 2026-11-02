use ruscodium::{
    cpp_adapter::{self, Options},
    parse, Model,
};

fn model(source: &str) -> Model {
    Model {
        schema_version: 1,
        files: vec![parse("input.lime", source, false).unwrap()],
    }
}
fn job(source: &str) -> Result<serde_json::Value, String> {
    cpp_adapter::build_job(&model(source), &Options::default())
}

#[test]
fn fresh_resolution_and_untrusted_shape_guards() {
    let source = "package sample\nstruct Item {\nvalue: Int\n}\nstruct Box {\nvalue: Item\n}\n";
    let mut m = model(source);
    m.files[0].declarations[1].children[0]
        .ty
        .as_mut()
        .unwrap()
        .resolved = Some("forged.Target".into());
    assert!(cpp_adapter::build_job(&m, &Options::default()).is_ok());
    m.files[0].declarations[1].children[0]
        .ty
        .as_mut()
        .unwrap()
        .builtin = true;
    assert!(cpp_adapter::build_job(&m, &Options::default()).is_err());
    let mut m = model(source);
    m.files[0].declarations[0].children.clear();
    assert!(cpp_adapter::build_job(&m, &Options::default()).is_err());
    let mut m = model(source);
    let forged = m.files[0].declarations[0].children[0].ty.clone().unwrap();
    m.files[0].declarations[0].children[0].parents.push(forged);
    assert!(cpp_adapter::build_job(&m, &Options::default()).is_err());
}

#[test]
fn literals_and_annotations_are_checked_before_mapping() {
    assert!(job("package sample\nstruct Item {\nvalue: Int = \"7\"\n}\n").is_err());
    assert!(job("package sample\nstruct Item {\nvalue: String = 7\n}\n").is_err());
    let mut m = model("package sample\nstruct Item {\nvalue: Int = 7\n}\n");
    m.files[0].declarations[0].children[0]
        .literal
        .as_mut()
        .unwrap()
        .kind = "boolean".into();
    assert!(cpp_adapter::build_job(&m, &Options::default()).is_err());
    let mut m = model("package sample\n@Cpp(\"Renamed\")\nclass Item {}\n");
    m.files[0].declarations[0].annotations[0]
        .raw
        .push_str("\nclass Injected {}");
    assert!(cpp_adapter::build_job(&m, &Options::default()).is_err());
    let annotation = model("package sample\n@Cpp(\"Renamed\")\nclass Item {}\n").files[0]
        .declarations[0]
        .annotations[0]
        .clone();
    let mut m = model("package sample\nlambda Item = (Int) -> Int\n");
    m.files[0].declarations[0].params[0]
        .annotations
        .push(annotation);
    assert!(cpp_adapter::build_job(&m, &Options::default()).is_err());
}

#[test]
fn retained_type_documentation_and_auxiliary_facts_are_checked() {
    let mut m = model("package sample\nstruct Item {\nvalue: Int\n}\n");
    m.files[0].declarations[0].children[0]
        .ty
        .as_mut()
        .unwrap()
        .docs
        .push("// type docs".into());
    assert!(cpp_adapter::build_job(&m, &Options::default()).is_err());
    let aux = parse("aux.lime", "package sample\n@Unknown\nclass Aux {}\n", true).unwrap();
    let mut m = model("package sample\nclass Main {}\n");
    m.files.push(aux);
    assert!(cpp_adapter::build_job(&m, &Options::default()).is_err());
    assert!(job("package sample\nstruct Item {\nvalue: List<// type doc\nInt>\n}\n").is_err());
}

#[test]
fn strict_options_are_validated_by_build_job() {
    let mut options = Options::default();
    options.root_namespace.push("class".into());
    assert!(cpp_adapter::build_job(&model("package sample\nclass Item {}\n"), &options).is_err());
}

#[test]
fn documentation_is_mapped_or_rejected_before_rendering() {
    let input = "package sample\n// A description.\n// @param[value] Input.\n// @return Output.\ninterface Item {\n    fun run(value: Int): Int\n}\n";
    // Function-specific blocks belong on the function itself.
    assert!(job(input).is_err());
    let input = "package sample\ninterface Item {\n// A description.\n// @param[value] Input.\n// @return Output.\nfun run(value: Int): Int\n}\n";
    let adapted = job(input).unwrap();
    let raw = adapted["raw_comments"].as_object().unwrap();
    assert!(raw
        .values()
        .any(|sections| sections.to_string().contains("Input")));
    assert!(raw
        .values()
        .any(|sections| sections.to_string().contains("Output")));
    assert!(job("package sample\n// {@Placeholder subject}\nclass Item {}\n").is_err());
}

#[test]
fn description_only_property_keeps_value_comment_empty() {
    let value =
        job("package sample\ninterface Item {\n// Property description.\nproperty value: Int\n}\n")
            .unwrap();
    let nodes = value["snapshot"]["nodes"].as_array().unwrap();
    let prop = nodes
        .iter()
        .find(|n| n["class"].as_str().unwrap().ends_with(".LimeProperty"))
        .unwrap();
    let raw = value["raw_comments"].as_object().unwrap();
    let comment = prop["properties"]["comment"]["$ref"].as_str().unwrap();
    let value_comment = prop["properties"]["valueComment"]["$ref"].as_str().unwrap();
    assert!(raw[comment].to_string().contains("Property description"));
    assert_eq!(raw[value_comment], serde_json::json!([]));
}

#[test]
fn documented_lambda_parameter_uses_owner_comment_path() {
    let adapted =
        job("package sample\n// @param[p0] Input.\nlambda Item = (Int) -> Int\n").unwrap();
    let nodes = adapted["snapshot"]["nodes"].as_array().unwrap();
    let node = |id: &str| nodes.iter().find(|n| n["id"] == id).unwrap();
    let param = nodes
        .iter()
        .find(|n| {
            n["class"]
                .as_str()
                .unwrap()
                .ends_with(".LimeLambdaParameter")
        })
        .unwrap();
    let comment = node(param["properties"]["comment"]["$ref"].as_str().unwrap());
    let path = node(comment["properties"]["path"]["$ref"].as_str().unwrap());
    assert_eq!(path["properties"]["tail"], serde_json::json!(["Item"]));
}

#[test]
fn cli_rejects_missing_values_before_writing() {
    let output = std::process::Command::new(env!("CARGO_BIN_EXE_ruscodium"))
        .args(["compile-cpp", "--input", "--output", "target/unused"])
        .output()
        .unwrap();
    assert!(!output.status.success());
    assert!(output.stdout.is_empty());
    assert!(String::from_utf8_lossy(&output.stderr).contains("missing argument"));
}

#[test]
fn enum_exceptions_reject_unbounded_native_models_and_reresolve_targets() {
    let source = "package sample\nenum Code { GOOD, BAD }\nexception Failure(Code)\ninterface Service { fun run(): Int throws Failure }\n";
    let mut m = model(source);
    let throws = m.files[0].declarations[2].children[0]
        .throws
        .as_mut()
        .unwrap();
    throws.resolved = Some("forged.Failure".into());
    assert!(cpp_adapter::generate(
        &m,
        "../gluecodium/src/main/resources/templates",
        &Options::default()
    )
    .is_ok());
    let mut m = model(source);
    m.files[0].declarations[1].ty.as_mut().unwrap().nullable = true;
    assert!(cpp_adapter::build_job(&m, &Options::default()).is_err());
    let mut m = model(source);
    m.files[0].declarations[2].children[0]
        .throws
        .as_mut()
        .unwrap()
        .nullable = true;
    assert!(cpp_adapter::build_job(&m, &Options::default()).is_err());
    assert!(job("package sample\ntypealias Alias = Int\nexception Failure(Alias)\n").is_err());
    assert!(job(
        "package sample\nenum Code { GOOD }\ntypealias Alias = Code\nexception Failure(Alias)\n"
    )
    .is_err());
    assert!(job("package sample\nexception Failure(Int)\n").is_err());
    assert!(job("package sample\nenum Code { GOOD }\nexception Failure(Code)\nstruct Box { item: List<Failure> }\n").is_err());
    let mut m = model(source);
    m.files[0].declarations[2].children[0].kind = "constructor".into();
    assert!(cpp_adapter::build_job(&m, &Options::default()).is_err());
}
