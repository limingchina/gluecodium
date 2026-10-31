use ruscodium::{parse, resolve, Model};
use std::{fs, path::PathBuf, process::Command};
fn model(text: &str) -> Model {
    Model {
        schema_version: 1,
        files: vec![parse("fixture.lime", text, false).unwrap()],
    }
}
#[test]
fn rejects_malformed_input() {
    for text in [
        "package x\nstruct A { x: String = \"bad\\q\" }\n",
        "package x\n/* unfinished",
        "package x\nstruct A { x: }\n",
    ] {
        assert!(parse("bad.lime", text, false).is_err(), "{text}");
    }
}
#[test]
fn resolution_and_cycles() {
    let mut m = model("package x\nstruct A { value: Missing }\n");
    assert!(resolve(&mut m).unwrap_err().contains("unresolved"));
    let mut m = model("package x\ntypealias A = B\ntypealias B = A\n");
    assert!(resolve(&mut m).unwrap_err().contains("cyclic"));
}
#[test]
fn ambiguity_in_all_scopes() {
    let mut m=model("package x\nstruct Thing { value: Int }\nclass Outer { struct Thing { value: Int } fun fetch(): Thing }\n");
    assert!(resolve(&mut m).unwrap_err().contains("ambiguous"));
}
#[test]
fn cpp_generation_compiles_and_runs() {
    let mut m=model("package sample\nstruct Point { x: Int y: Int }\ninterface Service { fun fetch(p: Point): Int }\n");
    resolve(&mut m).unwrap();
    let header = ruscodium::cpp::generate(&m).unwrap();
    let dir = std::env::temp_dir().join(format!("ruscodium-test-{}", std::process::id()));
    fs::create_dir_all(&dir).unwrap();
    fs::write(dir.join("api.hpp"), header).unwrap();
    fs::write(dir.join("main.cpp"),"#include \"api.hpp\"\nstruct S : sample::Service { int fetch(sample::Point p) override { return p.x + p.y; } };\nint main() { S s; return s.fetch({1,2}) == 3 ? 0 : 1; }\n").unwrap();
    let result = Command::new("c++")
        .current_dir(&dir)
        .args([
            "-std=c++17",
            "-Wall",
            "-Wextra",
            "-Werror",
            "main.cpp",
            "-o",
            "app",
        ])
        .status()
        .unwrap();
    assert!(result.success());
    assert!(Command::new(dir.join("app")).status().unwrap().success());
    fs::remove_dir_all(dir).unwrap();
}
#[test]
fn tracked_corpus_parses() {
    let root = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .to_owned();
    let out = Command::new("git")
        .current_dir(&root)
        .args(["ls-files", "*.lime"])
        .output()
        .unwrap();
    assert!(out.status.success());
    let listing = String::from_utf8(out.stdout).unwrap();
    let files: Vec<_> = listing.lines().collect();
    assert_eq!(files.len(), 345);
    for path in files {
        let text = fs::read_to_string(root.join(path)).unwrap();
        if let Err(e) = parse(path, &text, false) {
            panic!("{e}")
        }
    }
}
