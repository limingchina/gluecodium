#![allow(dead_code)]
mod template {
 #[path="@GRAPH_SOURCE@"] pub mod graph;
 #[path="@COMMENTS_SOURCE@"] mod native_comments;
 pub fn format(input:&str)->Result<String,String> { native_comments::format_with_references(input,"",&std::collections::BTreeMap::new(),false) }
}
fn main() {
 let args=std::env::args().collect::<Vec<_>>();
 let output=std::path::Path::new(&args[2]);std::fs::create_dir_all(output).unwrap();
 let mut paths=std::fs::read_dir(&args[1]).unwrap().map(|x|x.unwrap().path()).collect::<Vec<_>>();paths.sort();
 for p in paths { if p.extension().and_then(|s|s.to_str())!=Some("md"){continue;}let input=std::fs::read_to_string(&p).unwrap();
 let result=std::panic::catch_unwind(||template::format(&input));
 match result {Ok(Ok(text))=>std::fs::write(output.join(p.file_name().unwrap()),text).unwrap(),Ok(Err(e))=>std::fs::write(output.join(p.file_name().unwrap()).with_extension("error"),e).unwrap(),Err(_)=>std::fs::write(output.join(p.file_name().unwrap()).with_extension("panic"),"panic").unwrap()}
 }
}
