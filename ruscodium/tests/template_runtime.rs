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
            "ruscodium-template-{}-{}",
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
        "T:A:1,T:B:2\n  one\n  two\nlate\n"
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
