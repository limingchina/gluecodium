import argparse, io, subprocess, tarfile
from pathlib import Path
parser = argparse.ArgumentParser(description='Create an instrumented baseline source tree; do not use its binary for timing.')
parser.add_argument('--repo', type=Path, required=True, help='gluecodium git root')
parser.add_argument('--work', type=Path, required=True, help='new destination directory')
parser.add_argument('--ref', default='15b1db4c48ef0fbf7a86aefa6750f6ebcd5a5e88')
args = parser.parse_args()
repo = args.repo.resolve(strict=True)
root = args.work.resolve()
root.mkdir(exist_ok=False)
archive=subprocess.check_output(['git','archive',args.ref,'ruscodium/src','ruscodium/Cargo.toml','ruscodium/Cargo.lock'],cwd=repo)
with tarfile.open(fileobj=io.BytesIO(archive)) as t:
    t.extractall(root,filter='data')
src=root/'ruscodium/src'
(src/'perf_counts.rs').write_text('''use std::sync::atomic::{AtomicU64, Ordering};
pub static IMPORTS: AtomicU64 = AtomicU64::new(0);
pub static ABSENCE_PROBES: AtomicU64 = AtomicU64::new(0);
pub static RESOLVERS: AtomicU64 = AtomicU64::new(0);
pub static PARTIAL_PARSES: AtomicU64 = AtomicU64::new(0);
pub struct Report;
impl Drop for Report {
    fn drop(&mut self) {
        eprintln!("{}", serde_json::json!({"graph_imports": IMPORTS.load(Ordering::Relaxed), "absence_node_probes": ABSENCE_PROBES.load(Ordering::Relaxed), "resolver_constructions": RESOLVERS.load(Ordering::Relaxed), "file_partial_parses": PARTIAL_PARSES.load(Ordering::Relaxed)}));
    }
}
''')
with (src/'lib.rs').open('a') as f: f.write('\npub mod perf_counts;\n')
def replace(path,before,after):
    p=src/path
    s=p.read_text()
    assert s.count(before)==1,(path,s.count(before))
    p.write_text(s.replace(before,after))
replace('main.rs','fn main() {','fn main() {\n    let _counts = ruscodium::perf_counts::Report;')
replace('template/graph.rs','        Ok(graph)','''        crate::perf_counts::IMPORTS.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
        let absent_names: usize = graph.absent.values().map(BTreeSet::len).sum();
        // Successful import proves every absence scan exhausted all nodes:
        // an early match would have returned a validation error.
        crate::perf_counts::ABSENCE_PROBES.fetch_add((graph.nodes.len() * absent_names) as u64, std::sync::atomic::Ordering::Relaxed);
        Ok(graph)''')
replace('template/native_cpp.rs','        Ok(Self { config, parents })','''        crate::perf_counts::RESOLVERS.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
        Ok(Self { config, parents })''')
replace('template/mod.rs','                parse(name, &source)?','''                crate::perf_counts::PARTIAL_PARSES.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                parse(name, &source)?''')
print(root/'ruscodium')
