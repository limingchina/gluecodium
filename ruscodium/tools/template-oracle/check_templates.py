#!/usr/bin/env python3
"""Ensure the oracle's classpath templates match every unchanged source template."""
from pathlib import Path
import glob
import sys
import zipfile

root = Path('gluecodium/src/main/resources/templates')
jars = glob.glob('gluecodium/build/install/gluecodium/lib/gluecodium-*.jar')
if len(jars) != 1:
    sys.exit(f'Expected one installed gluecodium jar; found {jars}')
files = sorted(root.rglob('*.mustache'))
if len(files) != 315:
    sys.exit(f'Expected 315 production templates; found {len(files)}')
with zipfile.ZipFile(jars[0]) as jar:
    source_names = {'templates/' + path.relative_to(root).as_posix() for path in files}
    jar_names = {name for name in jar.namelist()
                 if name.startswith('templates/') and name.endswith('.mustache')}
    if jar_names != source_names:
        sys.exit(f'Installed template set differs: missing {sorted(source_names - jar_names)}, '
                 f'extra {sorted(jar_names - source_names)}')
    for path in files:
        name = 'templates/' + path.relative_to(root).as_posix()
        try:
            actual = jar.read(name)
        except KeyError:
            sys.exit(f'Installed jar is missing {name}')
        if actual != path.read_bytes():
            sys.exit(f'Installed template differs from source: {name}')
print(f'Checked {len(files)} installed templates against source')
