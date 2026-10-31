use std::{env, fs, path::PathBuf, process};
fn run() -> Result<(), String> {
    if env::args().nth(1).as_deref() == Some("render") {
        return render_cli();
    }
    let mut inputs = Vec::new();
    let mut aux = Vec::new();
    let mut output = None;
    let mut mode = "validate".to_string();
    let mut syntax = false;
    let args: Vec<_> = env::args().skip(1).collect();
    let mut i = 0;
    while i < args.len() {
        let a = &args[i];
        match a.as_str() {
            "-h" | "-help" | "--help" => {
                println!("ruscodium 0.1.0\nUsage: ruscodium -input PATH [-input PATH] [-auxinput PATH] [-validate | --syntax-only | -generators json|cpp -output DIR]\nOptions: --help --version --input --auxinput --output --validate --syntax-only --model --generators");
                return Ok(());
            }
            "--version" | "-version" => {
                println!("ruscodium 0.1.0");
                return Ok(());
            }
            "--syntax-only" => syntax = true,
            "--model" => mode = "model".into(),
            "-validate" | "--validate" => mode = "validate".into(),
            "-input" | "--input" | "-auxinput" | "--auxinput" | "-output" | "--output"
            | "-generators" | "--generators" => {
                i += 1;
                let v = args
                    .get(i)
                    .ok_or_else(|| format!("missing argument for {a}"))?;
                match a.as_str() {
                    "-input" | "--input" => inputs.push(PathBuf::from(v)),
                    "-auxinput" | "--auxinput" => aux.push(PathBuf::from(v)),
                    "-output" | "--output" => output = Some(PathBuf::from(v)),
                    _ => {
                        if v != "json" && v != "cpp" {
                            return Err(format!("unsupported generator: {v}"));
                        }
                        mode = v.clone()
                    }
                }
            }
            _ => return Err(format!("unknown option: {a}")),
        }
        i += 1
    }
    if syntax && (mode == "cpp" || mode == "json") {
        return Err("--syntax-only cannot be combined with a generator".into());
    }
    if inputs.is_empty() {
        return Err("at least one -input is required".into());
    }
    let mut model = ruscodium::load(&inputs, &aux)?;
    if model.files.is_empty() {
        return Err("no .lime input files found".into());
    }
    if !syntax {
        ruscodium::resolve(&mut model)?
    }
    if mode == "model" {
        println!(
            "{}",
            serde_json::to_string_pretty(&model).map_err(|e| e.to_string())?
        )
    } else if mode == "json" || mode == "cpp" {
        let dir = output.ok_or("generation requires -output")?;
        let json = if mode == "cpp" {
            ruscodium::cpp::generate(&model)?
        } else {
            serde_json::to_string_pretty(&model).map_err(|e| e.to_string())?
        };
        fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
        fs::write(
            dir.join(if mode == "cpp" {
                "api.hpp"
            } else {
                "model.json"
            }),
            format!("{json}\n"),
        )
        .map_err(|e| e.to_string())?;
    }
    Ok(())
}
fn main() {
    if let Err(e) = run() {
        eprintln!("{e}");
        process::exit(1)
    }
}

fn render_cli() -> Result<(), String> {
    let mut templates = None;
    let mut request = None;
    let mut output = None;
    let mut args = env::args().skip(2);
    while let Some(arg) = args.next() {
        let value = args
            .next()
            .ok_or_else(|| format!("missing argument for {arg}"))?;
        match arg.as_str() {
            "--templates" => templates = Some(PathBuf::from(value)),
            "--request" => request = Some(PathBuf::from(value)),
            "--output" => output = Some(PathBuf::from(value)),
            _ => return Err(format!("unknown render option: {arg}")),
        }
    }
    let templates = templates.ok_or("render requires --templates")?;
    let request = request.ok_or("render requires --request")?;
    let bytes = fs::read(&request).map_err(|e| format!("request: {e}"))?;
    if bytes.len() > 64 * 1024 * 1024 {
        return Err("request exceeds size limit".into());
    }
    let value = serde_json::from_slice(&bytes).map_err(|e| format!("request JSON: {e}"))?;
    let rendered = ruscodium::template::render(templates, &value)?;
    if let Some(path) = output {
        fs::write(path, rendered).map_err(|e| format!("output: {e}"))?;
    } else {
        use std::io::Write;
        std::io::stdout()
            .write_all(rendered.as_bytes())
            .map_err(|e| e.to_string())?;
    }
    Ok(())
}
