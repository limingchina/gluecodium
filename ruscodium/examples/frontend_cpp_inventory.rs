//! Verification-only native model and generated-file inventory.
//! No reference model, capture, or output inventory is read by this example.
use std::{env, fs, path::PathBuf};

fn run() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<_> = env::args().skip(1).collect();
    if args.len() != 5 {
        return Err("expected GROUP MAIN AUX-OR-- TEMPLATES OUTPUT".into());
    }
    let mut options = ruscodium::cpp_adapter::Options::default();
    if args[0] == "custom" {
        options.root_namespace = vec!["acme".into(), "api".into()];
        options.internal_namespace = vec!["acme".into(), "detail".into()];
        options.export = "ACME_API".into();
        options.export_common = Some("ACME_COMMON".into());
        options.copyright_header = Some("Copyright 2026 Example\nAll rights reserved.".into());
    } else if args[0] == "docs" {
        options.internal_namespace = vec!["gluecodium".into()];
    } else if args[0] != "default" {
        return Err("group must be default, custom or docs".into());
    }
    let main = vec![PathBuf::from(&args[1])];
    let aux = if args[2] == "-" {
        vec![]
    } else {
        vec![PathBuf::from(&args[2])]
    };
    let mut model = ruscodium::load(&main, &aux)?;
    ruscodium::resolve(&mut model)?;
    let job = ruscodium::cpp_adapter::build_job(&model, &options)?;
    let files = ruscodium::cpp_adapter::generate(&model, &args[3], &options)?;
    let output = PathBuf::from(&args[4]);
    fs::create_dir_all(&output)?;
    ruscodium::cpp_generation::write_files(output.join("files"), &files)?;
    let inventory: std::collections::BTreeMap<_, _> = files
        .iter()
        .map(|file| (file.path.to_string_lossy().into_owned(), &file.source_set))
        .collect();
    if inventory.len() != files.len() {
        return Err("duplicate generated path".into());
    }
    fs::write(output.join("job.json"), serde_json::to_vec_pretty(&job)?)?;
    fs::write(
        output.join("manifest.json"),
        serde_json::to_vec_pretty(&serde_json::json!({"files": inventory}))?,
    )?;
    Ok(())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("{error}");
        std::process::exit(1);
    }
}
