//! Verification-only complete native generation inventory, including source sets.
use std::{env, fs};
fn run() -> Result<(), Box<dyn std::error::Error>> {
    let mut args = env::args().skip(1);
    let job = args.next().ok_or("expected job path")?;
    let templates = args.next().ok_or("expected templates path")?;
    if args.next().is_some() {
        return Err("unexpected argument".into());
    }
    let value = serde_json::from_slice(&fs::read(job)?)?;
    let files = ruscodium::cpp_generation::generate(templates, &value)?;
    println!("{}", serde_json::to_string(&files)?);
    Ok(())
}
fn main() {
    if let Err(error) = run() {
        eprintln!("{error}");
        std::process::exit(1);
    }
}
