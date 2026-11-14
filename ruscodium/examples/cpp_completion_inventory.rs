//! Verification-only inventory for the native LIME-to-C++ pipeline.
use std::{env, fs, path::PathBuf};
fn run() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<_> = env::args_os().skip(1).collect();
    if args.len() != 2 { return Err("usage: cpp_completion_inventory INPUTS_JSON TEMPLATES".into()); }
    let request: serde_json::Value = serde_json::from_slice(&fs::read(&args[0])?)?;
    let paths = |key: &str| -> Result<Vec<PathBuf>, Box<dyn std::error::Error>> {
        request[key].as_array().ok_or("missing paths")?.iter()
            .map(|value| value.as_str().map(PathBuf::from).ok_or_else(|| "invalid path".into())).collect()
    };
    let inputs = paths("main")?; let aux = paths("aux")?;
    let options: ruscodium::cpp_adapter::Options = serde_json::from_value(request["options"].clone())?;
    let model = ruscodium::load(&inputs, &aux)?;
    let files = ruscodium::cpp_adapter::generate(&model, PathBuf::from(&args[1]), &options)?;
    println!("{}", serde_json::to_string(&files)?); Ok(())
}
fn main() { if let Err(error) = run() { eprintln!("{error}"); std::process::exit(1); } }
