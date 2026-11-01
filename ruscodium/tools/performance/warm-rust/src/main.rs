use std::{env, path::PathBuf, time::Instant};
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 5 { return Err("INPUT OUTPUT_BASE ITERATIONS TEMPLATES".into()); }
    let inputs = [PathBuf::from(&args[1])];
    let output = PathBuf::from(&args[2]);
    let iterations: usize = args[3].parse()?;
    let templates = PathBuf::from(&args[4]);
    let options = ruscodium::cpp_adapter::Options::default();
    for i in 0..iterations {
        let target = output.join(i.to_string());
        let start = Instant::now();
        let model = ruscodium::load(&inputs, &[])?;
        let files = ruscodium::cpp_adapter::generate(&model, &templates, &options)?;
        ruscodium::cpp_generation::write_files(target, &files)?;
        println!("{} {} true", i, start.elapsed().as_nanos());
    }
    Ok(())
}
