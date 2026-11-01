use std::{env, fs, path::PathBuf, process};

#[derive(serde::Deserialize)]
#[serde(deny_unknown_fields)]
struct NativeCppOptionsFile {
    schema: String,
    version: u64,
    #[serde(default)]
    root_namespace: Vec<String>,
    #[serde(default)]
    internal_namespace: Vec<String>,
    #[serde(default = "native_default_export")]
    export: String,
    #[serde(default)]
    export_common: Option<String>,
    #[serde(default)]
    copyright_header: Option<String>,
}
fn native_default_export() -> String {
    "_GLUECODIUM_CPP".into()
}
fn run() -> Result<(), String> {
    if env::args().nth(1).as_deref() == Some("compile-cpp") {
        return compile_cpp_cli();
    }
    if env::args().nth(1).as_deref() == Some("generate-cpp") {
        return generate_cpp_cli();
    }
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
                println!("ruscodium 0.1.0\nUsage: ruscodium -input PATH [-input PATH] [-auxinput PATH] [-validate | --syntax-only | -generators json|cpp -output DIR]\n       ruscodium render --templates DIR --request FILE [--output FILE]\n       ruscodium generate-cpp --job FILE --templates DIR --output DIR\n       ruscodium compile-cpp --input PATH [--auxinput PATH] --templates DIR --output DIR [--options FILE]\nOptions: --help --version --input --auxinput --output --validate --syntax-only --model --generators\nRun 'ruscodium render --help' for the experimental template renderer.");
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

fn compile_cpp_cli() -> Result<(), String> {
    let mut inputs = Vec::new();
    let mut aux = Vec::new();
    let (mut templates, mut output, mut options) = (None, None, None);
    let mut args = env::args().skip(2);
    while let Some(arg) = args.next() {
        if arg == "--help" || arg == "-h" {
            println!("Usage: ruscodium compile-cpp --input PATH [--input PATH] [--auxinput PATH] --templates DIR --output DIR [--options FILE]");
            return Ok(());
        }
        if !matches!(
            arg.as_str(),
            "--input" | "--auxinput" | "--templates" | "--output" | "--options"
        ) {
            return Err(format!("unknown compile-cpp option: {arg}"));
        }
        let value = PathBuf::from(
            args.next()
                .filter(|v| !v.starts_with('-'))
                .ok_or_else(|| format!("missing argument for {arg}"))?,
        );
        match arg.as_str() {
            "--input" => inputs.push(value),
            "--auxinput" => aux.push(value),
            _ => {
                let slot = match arg.as_str() {
                    "--templates" => &mut templates,
                    "--output" => &mut output,
                    _ => &mut options,
                };
                if slot.replace(value).is_some() {
                    return Err(format!("duplicate option: {arg}"));
                }
            }
        }
    }
    if inputs.is_empty() {
        return Err("compile-cpp requires --input".into());
    }
    let templates = templates.ok_or("compile-cpp requires --templates")?;
    let output = output.ok_or("compile-cpp requires --output")?;
    let options = if let Some(path) = options {
        let bytes = fs::read(path).map_err(|e| format!("options: {e}"))?;
        if bytes.len() > 1024 * 1024 {
            return Err("options exceed size limit".into());
        }
        let value: NativeCppOptionsFile =
            serde_json::from_slice(&bytes).map_err(|e| format!("options JSON: {e}"))?;
        if value.schema != "gluecodium.native-cpp-options" || value.version != 1 {
            return Err("unsupported native C++ options schema or version".into());
        }
        ruscodium::cpp_adapter::Options {
            root_namespace: value.root_namespace,
            internal_namespace: value.internal_namespace,
            export: value.export,
            export_common: value.export_common,
            copyright_header: value.copyright_header,
        }
    } else {
        ruscodium::cpp_adapter::Options::default()
    };
    let model = ruscodium::load(&inputs, &aux)?;
    let files = ruscodium::cpp_adapter::generate(&model, templates, &options)?;
    ruscodium::cpp_generation::write_files(output, &files)
}

fn generate_cpp_cli() -> Result<(), String> {
    let mut templates = None;
    let mut job = None;
    let mut output = None;
    let mut args = env::args().skip(2);
    while let Some(arg) = args.next() {
        if arg == "--help" || arg == "-h" {
            println!("Usage: ruscodium generate-cpp --job FILE --templates DIR --output DIR");
            return Ok(());
        }
        if !matches!(arg.as_str(), "--job" | "--templates" | "--output") {
            return Err(format!("unknown generate-cpp option: {arg}"));
        }
        let value = PathBuf::from(
            args.next()
                .ok_or_else(|| format!("missing argument for {arg}"))?,
        );
        let target = match arg.as_str() {
            "--job" => &mut job,
            "--templates" => &mut templates,
            _ => &mut output,
        };
        if target.replace(value).is_some() {
            return Err(format!("duplicate option: {arg}"));
        }
    }
    let templates = templates.ok_or("generate-cpp requires --templates")?;
    let path = job.ok_or("generate-cpp requires --job")?;
    let output = output.ok_or("generate-cpp requires --output")?;
    let bytes = fs::read(path).map_err(|e| format!("job: {e}"))?;
    if bytes.len() > 64 * 1024 * 1024 {
        return Err("job exceeds size limit".into());
    }
    let value = serde_json::from_slice(&bytes).map_err(|e| format!("job JSON: {e}"))?;
    let files = ruscodium::cpp_generation::generate(templates, &value)?;
    ruscodium::cpp_generation::write_files(output, &files)
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
        if arg == "--help" || arg == "-h" {
            println!("Usage: ruscodium render --templates DIR --request FILE [--output FILE]\nRender a version 1 template request. Without --output, write the result to stdout.");
            return Ok(());
        }
        if !matches!(arg.as_str(), "--templates" | "--request" | "--output") {
            return Err(format!("unknown render option: {arg}"));
        }
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
