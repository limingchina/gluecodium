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
    let mut m = model("package x\nstruct A {\n value: Missing\n }\n");
    assert!(resolve(&mut m).unwrap_err().contains("unresolved"));
    let mut m = model("package x\ntypealias A = B\ntypealias B = A\n");
    assert!(resolve(&mut m).unwrap_err().contains("cyclic"));
}
#[test]
fn ambiguity_in_all_scopes() {
    let mut m=model("package x\nstruct Thing {\n value: Int\n }\nclass Outer { struct Thing {\n value: Int\n }\n fun fetch(): Thing }\n");
    assert!(resolve(&mut m).unwrap_err().contains("ambiguous"));
}
#[test]
fn cpp_generation_compiles_and_runs() {
    let mut m=model("package sample\nstruct Point {\n x: Int\n y: Int\n }\ninterface Service { fun fetch(p: Point): Int }\n");
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
    let files: Vec<_> = listing
        .lines()
        .filter(|p| !p.starts_with("ruscodium/"))
        .collect();
    assert_eq!(files.len(), 345);
    for path in files {
        let text = fs::read_to_string(root.join(path)).unwrap();
        if let Err(e) = parse(path, &text, false) {
            panic!("{e}")
        }
    }
}

#[test]
fn repository_cpp_fixture_and_multiple_inputs() {
    let root = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .to_owned();
    let paths = [
        "cmake/tests/unit/gluecodium_generate/cpp-export/lime/common_main_foo.lime",
        "cmake/tests/unit/gluecodium_generate/cpp-export/lime/main_bar.lime",
    ]
    .map(|p| root.join(p));
    let mut m = ruscodium::load(&paths, &[]).unwrap();
    resolve(&mut m).unwrap();
    let header = ruscodium::cpp::generate(&m).unwrap();
    let dir = std::env::temp_dir().join(format!("ruscodium-repo-{}", std::process::id()));
    fs::create_dir_all(&dir).unwrap();
    fs::write(dir.join("api.hpp"), header).unwrap();
    fs::write(dir.join("main.cpp"),"#include \"api.hpp\"\nint main() { unit::test::CommonMainFoo* p = nullptr; return p != nullptr; }\n").unwrap();
    assert!(Command::new("c++")
        .current_dir(&dir)
        .args([
            "-std=c++17",
            "-Wall",
            "-Wextra",
            "-Werror",
            "main.cpp",
            "-o",
            "app"
        ])
        .status()
        .unwrap()
        .success());
    assert!(Command::new(dir.join("app")).status().unwrap().success());
    fs::remove_dir_all(dir).unwrap();
}
#[test]
fn unsupported_backend_does_not_write_output() {
    let dir = std::env::temp_dir().join(format!("ruscodium cli {}", std::process::id()));
    fs::create_dir_all(&dir).unwrap();
    let input = dir.join("input.lime");
    fs::write(
        &input,
        "package x\n@Something\nstruct A {\n value: Int\n }\n",
    )
    .unwrap();
    let out = dir.join("out");
    let status = Command::new(env!("CARGO_BIN_EXE_ruscodium"))
        .args([
            "-input",
            input.to_str().unwrap(),
            "-generators",
            "cpp",
            "-output",
            out.to_str().unwrap(),
        ])
        .status()
        .unwrap();
    assert!(!status.success());
    assert!(!out.exists());
    fs::remove_dir_all(dir).unwrap();
}

#[test]
fn coherent_repository_models() {
    let root = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .to_owned();
    let smoke = root.join("gluecodium/src/test/resources/smoke");
    for scenario in ["generic_types", "expose_internals", "basic_types", "async"] {
        let base = smoke.join(scenario);
        let auxiliary = base.join("auxiliary");
        let aux = if auxiliary.exists() {
            vec![auxiliary]
        } else {
            vec![]
        };
        let mut m = ruscodium::load(&[base.join("input")], &aux).unwrap();
        if let Err(e) = resolve(&mut m) {
            panic!("{scenario}: {e}")
        }
    }
    let mut calculator = ruscodium::load(&[root.join("examples/calculator/lime")], &[]).unwrap();
    resolve(&mut calculator).unwrap();
}
#[test]
fn reserved_words_newlines_and_alias_overloads() {
    assert!(parse("x", "package x class Foo {}\n", false).is_err());
    assert!(parse("x", "package x\nclass get {}\n", false).is_err());
    let mut m =
        model("package x\ntypealias Count = Int\nclass A { fun f(a: Int) fun f(a: Count) }\n");
    assert!(resolve(&mut m).unwrap_err().contains("duplicate signature"));
}

#[test]
fn literal_tree_and_syntax_guards() {
    let f = parse(
        "x",
        "package x\nstruct S {\n list: List<Int> = [1, 2]\n}\n",
        false,
    )
    .unwrap();
    let literal = f.declarations[0].children[0].literal.as_ref().unwrap();
    assert_eq!(literal.kind, "list");
    assert_eq!(literal.children.len(), 2);
    for bad in [
        "package x\nfun f()\n",
        "package x\nstruct S {}\n",
        "package x\nstruct S { x: Int = 1abc }\n",
        "package x\nstruct S { x: Int = [1, 2: 3] }\n",
    ] {
        assert!(parse("x", bad, false).is_err(), "{bad}");
    }
    let mut m = model("package x\nstruct `A` { n: Int }\nstruct B { a: A }\n");
    assert!(resolve(&mut m).is_ok());
}

#[test]
fn annotation_and_descriptor_structure() {
    let f = parse(
        "x",
        "package x\n@Tag(name = [\"a\", \"b\"])\nclass Foo {\n external { cpp name \"Foo\" }\n}\n",
        false,
    )
    .unwrap();
    let d = &f.declarations[0];
    assert_eq!(d.annotations[0].name, "Tag");
    assert_eq!(d.annotations[0].values[0].values.len(), 2);
    assert_eq!(d.descriptor.as_ref().unwrap().values[0].platform, "cpp");
}

#[test]
fn inheritance_constraints() {
    let mut m = model("package x\nclass Base {}\nclass Child : Base {}\n");
    assert!(resolve(&mut m).unwrap_err().contains("open"));
    let mut m = model(
        "package x\nopen class Base {}\nnarrow interface Extra {}\nclass Child : Base, Extra {}\n",
    );
    assert!(resolve(&mut m).is_ok());
    let mut m = model("package x\ninterface A {}\ninterface B {}\ninterface C : A, B {}\n");
    assert!(resolve(&mut m).unwrap_err().contains("narrow"));
}

#[test]
fn review_regressions() {
    let mut m = model("package x\ninterface A { property p: Int\n}\n");
    resolve(&mut m).unwrap();
    assert!(ruscodium::cpp::generate(&m).unwrap().contains("set_p"));
    for text in [
        "package x\nstruct char16_t { v: Int }\n",
        "package x\nclass A { fun A() }\n",
    ] {
        let mut m = model(text);
        resolve(&mut m).unwrap();
        assert!(ruscodium::cpp::generate(&m).is_err());
    }
    let mut m = model("package x\nstruct A { v: List<Void> }\n");
    assert!(resolve(&mut m).is_err());
    let mut m = model("package x\ntypealias N = Int?\nstruct A { v: N = null }\n");
    assert!(resolve(&mut m).is_ok());
    let mut m = model("package x\ntypealias N = Int?\nclass A { fun f(v: N) fun f(v: N?) }\n");
    assert!(resolve(&mut m).unwrap_err().contains("duplicate signature"));
}
#[test]
fn syntax_only_cannot_generate() {
    let input = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../examples/calculator/lime");
    let dir = std::env::temp_dir().join(format!("ruscodium-syntax-only-{}", std::process::id()));
    let result = Command::new(env!("CARGO_BIN_EXE_ruscodium"))
        .args([
            "-input",
            input.to_str().unwrap(),
            "--syntax-only",
            "-generators",
            "cpp",
            "-output",
            dir.to_str().unwrap(),
        ])
        .output()
        .unwrap();
    assert!(!result.status.success());
    assert!(!dir.exists());
}
#[test]
fn oracle_syntax_rejections() {
    for text in [
        "package x\nclass A { constructor make(): Int }\n",
        "package x\nclass A { property v: Int = 1\n}\n",
        "package x\nclass A { const X: Int\n}\n",
        "package x\nclass A { property v: Int { set }\n}\n",
        "package x\nstruct S { v: Int = class }\n",
        "package x\nstruct S { v: Int = Foo(1.5) }\n",
    ] {
        assert!(parse("x", text, false).is_err(), "{text}");
    }
}
