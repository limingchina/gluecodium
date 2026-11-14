"""Evidence identity for native sources, tools, templates and JVM jars."""
import hashlib
from pathlib import Path
import subprocess
ROOT = Path(__file__).resolve().parents[3]
RUST = ROOT / 'ruscodium'
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def identity():
    paths = [RUST / 'Cargo.toml', RUST / 'Cargo.lock']
    for name in ('src', 'examples', 'tools/cpp-completion'):
        paths.extend(p for p in (RUST/name).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    paths.extend(p for p in (ROOT/'gluecodium/src/main/resources/templates').rglob('*') if p.is_file())
    paths.extend(p for p in (ROOT/'gluecodium/build/install/gluecodium/lib').glob('*.jar') if p.is_file())
    def git(*args): return subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return {'git_head':git('rev-parse','HEAD').strip(),'git_status':git('status','--porcelain').splitlines(),
            'files_sha256':{str(p.relative_to(ROOT)):digest(p) for p in sorted(set(paths))}}
