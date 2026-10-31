use ruscodium::template::{parse, render, Graph};
use serde_json::{json, Value};
use std::{
    fs,
    path::{Path, PathBuf},
    sync::atomic::{AtomicUsize, Ordering},
};
static COUNTER: AtomicUsize = AtomicUsize::new(0);
struct Dir(PathBuf);
impl Dir {
    fn new() -> Self {
        let p = std::env::temp_dir().join(format!(
            "ruscodium template-{}-{}",
            std::process::id(),
            COUNTER.fetch_add(1, Ordering::Relaxed)
        ));
        fs::create_dir_all(&p).unwrap();
        Self(p)
    }
    fn write(&self, name: &str, content: &str) {
        let p = self.0.join(format!("{name}.mustache"));
        fs::create_dir_all(p.parent().unwrap()).unwrap();
        fs::write(p, content).unwrap();
    }
}
impl Drop for Dir {
    fn drop(&mut self) {
        fs::remove_dir_all(&self.0).unwrap();
    }
}
fn req(template: &str, data: Value) -> Value {
    json!({"schema":"gluecodium.template.render-request","version":1,"template":template,"data":data})
}
fn render_str(template: &str, data: Value) -> Result<String, String> {
    let d = Dir::new();
    d.write("test", template);
    render(&d.0, &req("test", data))
}
#[test]
fn production_templates_parse() {
    fn scan(path: &Path, count: &mut usize) {
        for entry in fs::read_dir(path).unwrap() {
            let path = entry.unwrap().path();
            if path.is_dir() {
                scan(&path, count);
            } else if path.extension().is_some_and(|x| x == "mustache") {
                *count += 1;
                parse(
                    &path.display().to_string(),
                    &fs::read_to_string(&path).unwrap(),
                )
                .unwrap();
            }
        }
    }
    let mut count = 0;
    scan(
        Path::new("../gluecodium/src/main/resources/templates"),
        &mut count,
    );
    assert_eq!(count, 315);
}
#[test]
fn sections_scope_partials_and_iterate() {
    let d = Dir::new();
    d.write("test", "{{!! comment !}}\n{{#set outer=title}}{{#items}}{{outer}}:{{name}}:{{iter.position}}{{#if iter.hasNext}},{{/if}}{{/items}}{{/set}}\n  {{>partial}}\n{{>late}}\n{{+late}}late{{/late}}\n");
    d.write("partial", "one\ntwo\n");
    assert_eq!(
        render(
            &d.0,
            &req(
                "test",
                json!({"title":"T","items":[{"name":"A"},{"name":"B"}]})
            )
        )
        .unwrap(),
        "T:A:0,T:B:1\n  one\n  two\nlate\n"
    );
}
#[test]
fn graph_identity_overlays_and_missing_properties() {
    let d = Dir::new();
    d.write(
        "test",
        "{{name}} {{next.name}} {{computed}} {{missingMap.key}}",
    );
    let mut r = req("test", json!({"$ref":"n1"}));
    r["snapshot"] = json!({"schema":"gluecodium.reference-model.snapshot","version":1,"root":{"$ref":"n1"},"nodes":[{"id":"n1","class":"LimeNode","properties":{"name":"A","next":{"$ref":"n2"},"missingMap":{}}},{"id":"n2","class":"LimeNode","properties":{"name":"B","next":{"$ref":"n1"}}}]});
    r["property_overlays"] = json!({"n1":{"computed":"C"}});
    assert_eq!(render(&d.0, &r).unwrap(), "A B C ");
    d.write("test", "{{unknown}}");
    assert!(render(&d.0, &r)
        .unwrap_err()
        .contains("unsupported property unknown"));
    r["snapshot"]["nodes"][1]["properties"]["next"] = json!({"$ref":"bad"});
    assert!(render(&d.0, &r).unwrap_err().contains("dangling"));
    r["snapshot"]["nodes"][1]["id"] = json!("n1");
    assert!(Graph::import(r.get("snapshot"), None)
        .unwrap_err()
        .contains("duplicate"));
}
#[test]
fn replay_and_helpers() {
    let d = Dir::new();
    d.write("test", "{{resolveName}} {{#ifPredicate \"test\"}}Y{{/ifPredicate}} {{#sort items sorter=\"s\"}}{{this}}{{/sort}} {{#filter items predicate=\"positive\"}}{{#this}}{{this}}{{/this}}{{/filter}} {{prefix text \"> \" skipFirstLine=true}}");
    let mut r = req("test", json!({"items":[1,2],"text":"a  \nb "}));
    r["hooks"] = json!({"names":[{"receiver":{"items":[1,2],"text":"a  \nb "},"resolver":"","mode":"name","result":"ok"}],"predicates":[{"receiver":{"items":[1,2],"text":"a  \nb "},"name":"test","result":true},{"receiver":1,"name":"positive","result":false},{"receiver":2,"name":"positive","result":true}],"sorters":[{"name":"s","input":[1,2],"result":[2,1]}]});
    assert_eq!(render(&d.0, &r).unwrap(), "ok Y 21 2 a\n> b");
    r["hooks"]["names"] = json!([]);
    assert!(render(&d.0, &r).unwrap_err().contains("missing replay"));
}
#[test]
fn path_and_recursion_limits() {
    let d = Dir::new();
    d.write("test", "{{>../outside}}");
    assert!(render(&d.0, &req("test", json!({})))
        .unwrap_err()
        .contains("invalid partial"));
    d.write("test", "{{>test}}");
    assert!(render(&d.0, &req("test", json!({})))
        .unwrap_err()
        .contains("recursion"));
    assert!(render_str("{{unknown x}}", json!({}))
        .unwrap_err()
        .contains("unsupported helper"));
}

#[test]
fn measured_absences_allow_fallback_but_cannot_hide_a_getter() {
    let d = Dir::new();
    d.write("test", "{{#nested}}{{ambient}}/{{this.ambient}}{{/nested}}");
    let mut r = req("test", json!({"ambient":"outer","nested":{"$ref":"n1"}}));
    r["snapshot"] = json!({"schema":"gluecodium.reference-model.snapshot","version":1,"root":{"$ref":"n1"},"nodes":[{"id":"n1","class":"Example","properties":{}}]});
    assert!(render(&d.0, &r).is_err());
    d.write("test", "{{#nested}}{{ambient}}{{/nested}}");
    assert!(render(&d.0, &r)
        .unwrap_err()
        .contains("unsupported property ambient"));
    d.write("test", "{{#nested}}{{ambient}}/{{this.ambient}}{{/nested}}");
    r["absent_properties"] = json!({"n1":["ambient"]});
    assert_eq!(render(&d.0, &r).unwrap(), "outer/");
    r["property_overlays"] = json!({"n1":{"ambient":"getter"}});
    assert!(render(&d.0, &r).unwrap_err().contains("conflicts"));
}
#[test]
fn cli_failure_does_not_truncate_output() {
    let d = Dir::new();
    d.write("test", "{{unimplemented value}}");
    let request = d.0.join("request.json");
    let output = d.0.join("out.txt");
    fs::write(
        &request,
        serde_json::to_vec(&req("test", json!({}))).unwrap(),
    )
    .unwrap();
    fs::write(&output, "preserve").unwrap();
    let status = std::process::Command::new(env!("CARGO_BIN_EXE_ruscodium"))
        .args(["render", "--templates"])
        .arg(&d.0)
        .arg("--request")
        .arg(&request)
        .arg("--output")
        .arg(&output)
        .status()
        .unwrap();
    assert!(!status.success());
    assert_eq!(fs::read_to_string(output).unwrap(), "preserve");
}
#[cfg(unix)]
#[test]
fn partial_symlink_cannot_escape_root() {
    let d = Dir::new();
    let outside = Dir::new();
    outside.write("secret", "outside");
    std::os::unix::fs::symlink(
        outside.0.join("secret.mustache"),
        d.0.join("secret.mustache"),
    )
    .unwrap();
    d.write("test", "{{>secret}}");
    assert!(render(&d.0, &req("test", json!({})))
        .unwrap_err()
        .contains("escapes template root"));
}
#[test]
fn dynamic_selectors_and_helper_conditions() {
    assert_eq!(render_str("{{#eval \"values\" key}}{{this}}{{/eval}} {{#if zero}}bad{{/if}}{{#zero}}ok{{/zero}} {{#switch n}}{{#case 1}}one{{/case}}{{#case 2}}two{{/case}}{{#default}}other{{/default}}{{/switch}}",json!({"values":{"a.b":"found"},"key":"a.b","zero":0,"n":2})).unwrap(),"found ok two");
}

#[test]
fn reject_nested_tag_delimiters() {
    assert!(parse("bad", "a{{!! before {{value}} after !}}b")
        .unwrap_err()
        .contains("nested tag delimiter"));
}

#[test]
fn measured_trimou_literal_iteration_and_flow() {
    assert_eq!(render_str(r#"{{prefix "a=b" "> "}}|{{prefix "a\nb" "> "}}|{{#isEq nil nil}}bad{{/isEq}}|{{#items}}{{iter.index}}:{{iter.position}};{{/items}}|{{#switch n}}{{#default}}D1{{/default}}{{#default}}D2{{/default}}{{/switch}}|{{capitalize "ßabc"}}"#, json!({"nil":null,"items":["a","b"],"n":1})).unwrap(), r#"> a=b|> a\nb||1:0;2:1;|D1|Ssabc"#);
}

#[test]
fn reject_measured_invalid_constructs() {
    for source in [
        "{{#if}}x{{/if}}",
        "{{#unless}}x{{/unless}}",
        "{{#set name}}x{{/set}}",
        "{{+p}}a{{/p}}{{+p}}b{{/p}}",
        "{{+p param}}x{{/p}}",
        "{{#no}}{{#if}}x{{/if}}{{/no}}",
        "{{#no}}{{prefix \"unterminated}}{{/no}}",
        "{{#no}}{{prefix}}{{/no}}",
        "{{#no}}{{capitalize}}{{/no}}",
        "{{#no}}{{join}}{{/no}}",
        "{{#no}}{{joinPartial}}{{/no}}",
        "{{#no}}{{if yes}}{{/no}}",
        "{{#no}}{{#setJoin \"x\" \"a\" delimiter=\",\"}}x{{/setJoin}}{{/no}}",
        "{{#setJoin \"x\" \"a\" \"b\"}}x{{/setJoin}}",
        "{{#set x=}}x{{/set}}",
    ] {
        assert!(parse("bad", source).is_err(), "accepted {source}");
    }
    assert!(
        render_str("{{#each name}}x{{/each}}", json!({"name":"text"}))
            .unwrap_err()
            .contains("iterable")
    );
    assert!(render_str("{{capitalize name}}", json!({"name":"ǳabc"}))
        .unwrap_err()
        .contains("Unicode titlecase"));
    assert!(render_str("{{this}}", json!({"x":1}))
        .unwrap_err()
        .contains("object string conversion"));
}

#[test]
fn reject_conflicting_hooks_before_output() {
    let d = Dir::new();
    d.write("test", "untouched");
    let mut r = req("test", json!({}));
    r["hooks"] = json!({"predicates":[{"receiver":{},"name":"p","result":true},{"receiver":{},"name":"p","result":false}]});
    assert!(render(&d.0, &r).unwrap_err().contains("conflicting hooks"));
    r["hooks"] = json!({"names":[{"receiver":{},"resolver":"r","mode":"wrong","result":"x"}]});
    assert!(render(&d.0, &r).unwrap_err().contains("invalid hooks"));
    r["hooks"] = json!({"sorters":[{"name":"s","input":[],"result":[{"$ref":"missing"}]}]});
    assert!(render(&d.0, &r).unwrap_err().contains("dangling"));
}

#[test]
fn empty_filter_requires_evidence_of_a_registered_predicate() {
    let d = Dir::new();
    d.write("test", "{{#filter items predicate=\"p\"}}yes{{/filter}}");
    let mut r = req("test", json!({"items":[]}));
    assert!(render(&d.0, &r).unwrap_err().contains("registration"));
    r["hooks"] = json!({"registered_predicates":["p"]});
    assert_eq!(render(&d.0, &r).unwrap(), "yes");
    r["hooks"] = json!({"registered_predicates":["p", "p"]});
    assert!(render(&d.0, &r).unwrap_err().contains("duplicate"));
    r["hooks"] = json!({"registered_predicates":["p"],"predicates":[]});
    r["data"]["items"] = json!([1]);
    assert!(render(&d.0, &r)
        .unwrap_err()
        .contains("missing replay predicate p for 1"));
}

#[test]
fn attribute_views_keep_case_insensitivity_without_changing_maps() {
    let d = Dir::new();
    d.write("test", "{{attrs.cpp.fullname}}/{{attrs.CPP.FullName}}/{{attrs.cpp.fullName}}/{{attrs.CPP.FULL_NAME}}/{{attrs.swift.optionSet}}/{{attrs.cpp.isEmpty}}/{{plain.Foo}}/{{plain.foo}}");
    let mut r = req("test", json!({"attrs":{"$ref":"a"},"plain":{"Foo":"yes"}}));
    r["snapshot"] = json!({"schema":"gluecodium.reference-model.snapshot","version":1,"root":{"$ref":"a"},"nodes":[{"id":"a","class":"com.here.gluecodium.model.lime.LimeAttributes","properties":{"attributes":{"CPP":{"FULL_NAME":"Foo"},"SWIFT":{"OPTION_SET":true}}}}]});
    assert_eq!(render(&d.0, &r).unwrap(), "Foo/Foo/Foo//true/false/yes/");
}

#[test]
fn sort_does_not_create_iteration_metadata_and_secondary_objects_fail() {
    let d = Dir::new();
    d.write(
        "test",
        "{{#sort items sorter=\"s\"}}{{this}}:{{iter.index}}/{{iter.position}};{{/sort}}",
    );
    let mut r = req("test", json!({"items":["a","b"]}));
    r["hooks"] = json!({"sorters":[{"name":"s","input":["a","b"],"result":["a","b"]}]});
    assert_eq!(render(&d.0, &r).unwrap(), "a:/;b:/;");
    for source in [
        "{{prefix \"a\" values}}",
        "{{+p}}X{{/p}}{{joinPartial items \"p\" values}}",
        "{{#setJoin values \"a\" \"b\" delimiter=\",\"}}{{this}}{{/setJoin}}",
    ] {
        assert!(
            render_str(source, json!({"values":{"x":1},"items":[1]}))
                .unwrap_err()
                .contains("object string conversion"),
            "{source}"
        );
    }
    assert!(render_str("{{joinPartial nil \"p\"}}", json!({"nil":null}))
        .unwrap_err()
        .contains("non-null"));
}

#[test]
fn cli_matches_all_jvm_goldens() {
    fn copy_tree(source: &Path, dest: &Path) {
        fs::create_dir_all(dest).unwrap();
        for entry in fs::read_dir(source).unwrap() {
            let entry = entry.unwrap();
            let target = dest.join(entry.file_name());
            if entry.path().is_dir() {
                copy_tree(&entry.path(), &target);
            } else {
                fs::copy(entry.path(), target).unwrap();
            }
        }
    }
    let d = Dir::new();
    copy_tree(
        Path::new("../gluecodium/src/main/resources/templates"),
        &d.0,
    );
    copy_tree(Path::new("tools/template-oracle/templates"), &d.0);
    let mut count = 0;
    for entry in fs::read_dir("tests/template-goldens").unwrap() {
        let path = entry.unwrap().path();
        let Some(name) = path.file_name().and_then(|s| s.to_str()) else {
            continue;
        };
        let Some(stem) = name.strip_suffix(".request.json") else {
            continue;
        };
        let actual = std::process::Command::new(env!("CARGO_BIN_EXE_ruscodium"))
            .arg("render")
            .arg("--templates")
            .arg(&d.0)
            .arg("--request")
            .arg(&path)
            .output()
            .unwrap();
        assert!(
            actual.status.success(),
            "{stem}: {}",
            String::from_utf8_lossy(&actual.stderr)
        );
        assert_eq!(
            actual.stdout,
            fs::read(path.with_file_name(format!("{stem}.expected"))).unwrap(),
            "{stem}"
        );
        count += 1;
    }
    assert!(count >= 27, "missing oracle fixtures: {count}");
}

#[test]
fn render_help_is_discoverable() {
    for args in [&["--help"][..], &["render", "--help"][..]] {
        let output = std::process::Command::new(env!("CARGO_BIN_EXE_ruscodium"))
            .args(args)
            .output()
            .unwrap();
        assert!(output.status.success());
        assert!(String::from_utf8(output.stdout).unwrap().contains("render"));
    }
}
