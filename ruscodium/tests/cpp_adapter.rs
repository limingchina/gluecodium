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
    assert!(cpp_adapter::build_job(&m, &Options::default()).is_ok());
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
    // Unmatched documentation blocks are retained as source documentation.
    assert!(job(input).is_ok());
    let input = "package sample\ninterface Item {\n// A description.\n// @param[value] Input.\n// @return Output.\nfun run(value: Int): Int\n}\n";
    let adapted = job(input).unwrap();
    let raw = adapted["raw_comments"].as_object().unwrap();
    assert!(raw
        .values()
        .any(|sections| sections.to_string().contains("Input")));
    assert!(raw
        .values()
        .any(|sections| sections.to_string().contains("Output")));
    assert!(job("package sample\n// {@Placeholder subject}\nclass Item {}\n").is_ok());
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
    assert!(job("package sample\ntypealias Alias = Int\nexception Failure(Alias)\n").is_ok());
    assert!(job(
        "package sample\nenum Code { GOOD }\ntypealias Alias = Code\nexception Failure(Alias)\n"
    )
    .is_ok());
    assert!(job("package sample\nexception Failure(Int)\n").is_ok());
    assert!(job("package sample\nenum Code { GOOD }\nexception Failure(Code)\nstruct Box { item: List<Failure> }\n").is_err());
    let mut m = model(source);
    m.files[0].declarations[2].children[0].kind = "constructor".into();
    assert!(cpp_adapter::build_job(&m, &Options::default()).is_err());
}

#[test]
fn native_filtering_precedes_resolution_and_strict_validation() {
    let source = "package sample\n@Skip(\"lite\")\n@Immutable\nstruct Removed { value: Missing }\nclass Kept {}\n";
    let options = Options {
        tags: vec!["LITE".into()],
        strict: true,
        ..Options::default()
    };
    assert!(cpp_adapter::build_job(&model(source), &options).is_ok());
    let source = "package sample\n@Skip(\"lite\")\n@Cpp(Skip)\nclass Removed {}\nclass Kept {}\n";
    assert!(cpp_adapter::build_job(&model(source), &options)
        .unwrap_err()
        .contains("C++ skip validation failed"));
}

#[test]
fn composite_literals_and_overload_parameter_paths_are_preserved() {
    let source = "package sample\nstruct Values { value: List<Int> = [1, 2] }\ninterface Service {\nfun run(a: Int)\nfun run(b: String)\n}\n";
    let value = job(source).unwrap();
    let nodes = value["snapshot"]["nodes"].as_array().unwrap();
    assert!(nodes.iter().any(|n| n["class"]
        .as_str()
        .unwrap()
        .ends_with("LimeValue$InitializerList")));
    let by_id = |id: &str| nodes.iter().find(|n| n["id"] == id).unwrap();
    let second = nodes
        .iter()
        .find(|n| {
            n["class"].as_str().unwrap().ends_with("LimeParameter") && {
                let path = by_id(n["properties"]["path"]["$ref"].as_str().unwrap());
                path["properties"]["tail"]
                    .as_array()
                    .unwrap()
                    .last()
                    .unwrap()
                    == "b"
            }
        })
        .unwrap();
    let path = by_id(second["properties"]["path"]["$ref"].as_str().unwrap());
    assert_eq!(path["properties"]["disambiguator"], "1");
}

#[test]
fn duplicate_type_names_get_unique_paths_for_cpp_generation() {
    let source =
        "package sample\n@Cpp(\"FirstThing\")\nclass Thing {}\nclass Thing { fun run() }\n";
    let m = model(source);
    let mut preview = m.clone();
    assert!(ruscodium::resolve(&mut preview).is_err());
    let v = cpp_adapter::build_job(&m, &Options::default()).unwrap();
    let nodes = v["snapshot"]["nodes"].as_array().unwrap();
    let paths: Vec<_> = nodes
        .iter()
        .filter(|n| n["class"].as_str().unwrap().ends_with("LimeClass"))
        .map(|n| {
            let id = n["properties"]["path"]["$ref"].as_str().unwrap();
            nodes.iter().find(|n| n["id"] == id).unwrap()["properties"]["disambiguator"]
                .as_str()
                .unwrap()
        })
        .collect();
    assert_eq!(paths, ["", "1"]);
}

#[test]
fn property_accessors_inherit_deprecation_and_keep_their_own_docs() {
    let source = "package sample\ninterface Service {\n@Deprecated(\"use other\")\nproperty item: Int {\n// Read the item.\nget\n// Write the item.\nset\n}\n}\n";
    let v = job(source).unwrap();
    let nodes = v["snapshot"]["nodes"].as_array().unwrap();
    let prop = nodes
        .iter()
        .find(|n| n["class"].as_str().unwrap().ends_with("LimeProperty"))
        .unwrap();
    for (accessor, text) in [("getter", "Read the item."), ("setter", "Write the item.")] {
        let id = prop["properties"][accessor]["$ref"].as_str().unwrap();
        let f = nodes.iter().find(|n| n["id"] == id).unwrap();
        let attr_id = f["properties"]["attributes"]["$ref"].as_str().unwrap();
        let attrs = nodes.iter().find(|n| n["id"] == attr_id).unwrap();
        assert!(attrs["properties"]["attributes"]["DEPRECATED"]["MESSAGE"].is_object());
        let comment = f["properties"]["comment"]["$ref"].as_str().unwrap();
        assert!(v["raw_comments"][comment].to_string().contains(text));
    }
}

#[test]
fn native_generation_surfaces_documentation_warnings_without_writing() {
    let m = model("package sample\n// A reference to [MissingType].\nclass Item {}\n");
    let templates = "../gluecodium/src/main/resources/templates";
    let (files, warnings) =
        cpp_adapter::generate_with_diagnostics(&m, templates, &Options::default()).unwrap();
    assert!(!files.is_empty());
    assert!(warnings.iter().any(|w| w.contains("MissingType")));
    let options = Options {
        werror: vec!["DocLinks".into()],
        ..Options::default()
    };
    assert!(cpp_adapter::generate_with_diagnostics(&m, templates, &options).is_err());
}

#[test]
fn multiline_string_value_preserves_its_source_content() {
    let value =
        job("package sample\nstruct Item { value: String = \"\"\"first\nsecond\"\"\" }\n").unwrap();
    let nodes = value["snapshot"]["nodes"].as_array().unwrap();
    assert!(nodes.iter().any(
        |n| n["class"].as_str().unwrap().ends_with("LimeValue$Literal")
            && n["properties"]["value"] == "first\nsecond"
    ));
}

#[test]
fn signed_special_values_allow_spacing() {
    let value = job("package sample\nstruct Item { value: Double = - Infinity }\n").unwrap();
    let nodes = value["snapshot"]["nodes"].as_array().unwrap();
    assert!(nodes.iter().any(
        |n| n["class"].as_str().unwrap().ends_with("LimeValue$Special")
            && n["properties"]["value"]["name"] == "NEGATIVE_INFINITY"
    ));
}

#[test]
fn positional_enumerator_resets_after_an_alias() {
    let value = job("package sample\nenum Other { VALUE = 42 }\nenum Code { ALIAS = Other.VALUE, NEXT }\nstruct Item { code: Code = Code(0) }\n").unwrap();
    let nodes = value["snapshot"]["nodes"].as_array().unwrap();
    let reference = nodes
        .iter()
        .find(|n| {
            n["class"]
                .as_str()
                .unwrap()
                .ends_with("LimePositionalEnumeratorRef")
        })
        .unwrap();
    let target = reference["properties"]["element"]["$ref"].as_str().unwrap();
    let node = nodes.iter().find(|n| n["id"] == target).unwrap();
    let path = node["properties"]["path"]["$ref"].as_str().unwrap();
    let path = nodes.iter().find(|n| n["id"] == path).unwrap();
    assert_eq!(
        path["properties"]["tail"]
            .as_array()
            .unwrap()
            .last()
            .unwrap(),
        "NEXT"
    );
}

#[test]
fn quoted_names_and_open_interfaces_are_supported() {
    let input = "package sample\n@Cpp(\"Safe\")\nstruct `name.with spaces` { @Cpp(\"safe\") `field-with-hyphen`: Int }\nopen narrow interface Listener {}\n";
    let m = model(input);
    assert!(cpp_adapter::generate(
        &m,
        "../gluecodium/src/main/resources/templates",
        &Options::default()
    )
    .is_ok());
}

#[test]
fn lime_strings_accept_literal_newlines_and_tabs() {
    let value =
        job("package sample\nstruct Item { value: String = \"line one\nline\ttwo\" }\n").unwrap();
    let nodes = value["snapshot"]["nodes"].as_array().unwrap();
    assert!(nodes.iter().any(
        |n| n["class"].as_str().unwrap().ends_with("LimeValue$Literal")
            && n["properties"]["value"] == "line one\nline\ttwo"
    ));
}

#[test]
fn field_constructor_reference_retains_annotations() {
    let value = job("package sample\nstruct Item {\nvalue: Int\nfield constructor(@Cpp(\"renamed\") value)\n}\n").unwrap();
    let nodes = value["snapshot"]["nodes"].as_array().unwrap();
    let field_ref = nodes
        .iter()
        .find(|n| n["class"].as_str().unwrap().ends_with("LimeLazyFieldRef"))
        .unwrap();
    let id = field_ref["properties"]["attributes"]["$ref"]
        .as_str()
        .unwrap();
    let attrs = nodes.iter().find(|n| n["id"] == id).unwrap();
    assert_eq!(attrs["properties"]["attributes"]["CPP"]["NAME"], "renamed");
}

#[test]
fn constructor_after_construction_retains_resolved_call_and_parameters() {
    let source = "package sample\nclass Item {\n@AfterConstruction(\"setup(this, value)\")\nconstructor make(value: Int)\nstatic fun setup(item: Item, value: Int)\n}\n";
    let value = job(source).unwrap();
    let nodes = value["snapshot"]["nodes"].as_array().unwrap();
    let call = nodes
        .iter()
        .find(|n| {
            n["class"]
                .as_str()
                .unwrap()
                .ends_with("LimeLazyFunctionCall")
        })
        .unwrap();
    assert_eq!(call["properties"]["elementFullName"], "sample.Item.setup");
    assert_eq!(
        call["properties"]["parameters"].as_array().unwrap().len(),
        2
    );
    assert!(cpp_adapter::generate(
        &model(source),
        "../gluecodium/src/main/resources/templates",
        &Options::default()
    )
    .is_ok());
}

#[test]
fn property_filter_keeps_getter_and_filters_setter() {
    let source = "package sample\ninterface Service {\nproperty value: Int {\n@Cpp(Skip)\nget\n@Skip(\"lite\")\nset\n}\n}\n";
    let options = Options {
        tags: vec!["lite".into()],
        ..Options::default()
    };
    let value = cpp_adapter::build_job(&model(source), &options).unwrap();
    let nodes = value["snapshot"]["nodes"].as_array().unwrap();
    let prop = nodes
        .iter()
        .find(|n| n["class"].as_str().unwrap().ends_with("LimeProperty"))
        .unwrap();
    assert!(prop["properties"]["getter"].is_object());
    assert!(prop["properties"]["setter"].is_null());
}

#[test]
fn imports_validate_before_tag_filter_and_types_resolve_after_it() {
    let main = parse(
        "main.lime",
        "package sample\nimport hidden.Hidden\nclass Item {}\n",
        false,
    )
    .unwrap();
    let hidden = parse(
        "hidden.lime",
        "package hidden\n@Skip(\"lite\")\nclass Hidden {}\n",
        false,
    )
    .unwrap();
    let options = Options {
        tags: vec!["lite".into()],
        ..Options::default()
    };
    let m = Model {
        schema_version: 1,
        files: vec![main, hidden],
    };
    assert!(cpp_adapter::build_job(&m, &options).is_ok());
    let mut missing = m.clone();
    missing.files[0].imports[0] = "hidden.Missing".into();
    assert!(cpp_adapter::build_job(&missing, &options)
        .unwrap_err()
        .contains("unresolved import"));
    let mut used = m.clone();
    used.files[0] = parse(
        "main.lime",
        "package sample\nimport hidden.Hidden\nstruct Item { value: Hidden }\n",
        false,
    )
    .unwrap();
    assert!(cpp_adapter::build_job(&used, &options)
        .unwrap_err()
        .contains("unresolved type"));
}
