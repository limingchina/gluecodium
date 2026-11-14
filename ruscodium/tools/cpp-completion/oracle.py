#!/usr/bin/env python3
"""Compare complete JVM C++ generation with native snapshot and LIME pipelines."""
import argparse, hashlib, json, os, shutil, subprocess, tempfile
from pathlib import Path
from provenance import identity
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
LIB=ROOT/'gluecodium/build/install/gluecodium/lib'
TEMPLATES=ROOT/'gluecodium/src/main/resources/templates'
SMOKE=ROOT/'gluecodium/src/test/resources/smoke'
def run(args,**kw):return subprocess.run([str(a) for a in args],cwd=ROOT,text=True,capture_output=True,**kw)
def read(path):return json.loads(path.read_text())
def write(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def tree(root):return {p.relative_to(root).as_posix():sha(p) for p in sorted(root.rglob('*')) if p.is_file()} if root.exists() else {}
def diff(a,b):return {'missing':sorted(a.keys()-b.keys()),'unexpected':sorted(b.keys()-a.keys()),'different':sorted(k for k in a.keys()&b.keys() if a[k]!=b[k])}
def inventory(binary,args,expected_sets,actual_files):
    result=run([binary,*args])
    if result.returncode:return {'status':'failure','diagnostic':result.stderr[-4000:]}
    entries=json.loads(result.stdout);sets={x['path']:x['source_set'] for x in entries};hashes={x['path']:hashlib.sha256(x['contents'].encode('utf-8')).hexdigest() for x in entries}
    a,b=diff(expected_sets,sets),diff(actual_files,hashes)
    return {'status':'match' if len(entries)==len(sets) and not any(a.values()) and not any(b.values()) else 'mismatch','source_sets':a,'cli_bytes':b}
def cpp_reference(p):return any(f.is_file() and not f.name.lower().startswith('ignore') for f in (p/'output/cpp').rglob('*'))
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--mode',required=True,choices=('smoke','functional'))
    for name in ('native','snapshot-inventory','lime-inventory','capture','report'):p.add_argument('--'+name,required=True,type=Path)
    p.add_argument('--revision',required=True);p.add_argument('--native-compiler',required=True);args=p.parse_args()
    capture=args.capture.resolve()
    if capture.exists() and any(capture.iterdir()):raise SystemExit('capture must be empty')
    capture.mkdir(parents=True,exist_ok=True);pin=capture/'_binaries';pin.mkdir()
    native,snap_inv,lime_inv=[Path(shutil.copy2(source.resolve(),pin/name)) for source,name in zip((args.native,args.snapshot_inventory,args.lime_inventory),('ruscodium','cpp_inventory','cpp_completion_inventory'))]
    before=identity();java=Path(os.environ['JAVA_HOME'])/'bin/java' if os.environ.get('JAVA_HOME') else 'java';javac=Path(os.environ['JAVA_HOME'])/'bin/javac' if os.environ.get('JAVA_HOME') else 'javac'
    if args.mode=='smoke':
        cases=sorted(p for p in SMOKE.iterdir() if p.is_dir()); cpp=[p for p in cases if cpp_reference(p)];strict=[p for p in cpp if (p/'input/validationfail.txt').exists()]
        if len(cases)<49 or len(cpp)<38 or {p.name for p in strict}!={'strict_fail_immutable','strict_fail_internal'}:raise SystemExit(f'incomplete inventory: {len(cases)} total, {len(cpp)} C++, {len(strict)} strict')
        names=[p.name for p in cases]
    else:
        result=run([HERE/'functional-inventory','--output',capture/'inventory'])
        if result.returncode:raise SystemExit(result.stderr)
        names=['functional','namerules']+list(read(capture/'inventory/functional-inventory.json')['targeted_probes'])
    rows=[]
    with tempfile.TemporaryDirectory(prefix='cpp-completion-') as temp:
        classes=Path(temp)/'classes';classes.mkdir();logging=Path(temp)/'logging.properties';logging.write_text('handlers=java.util.logging.ConsoleHandler\n.level=WARNING\n')
        result=run([javac,'-cp',LIB/'*','-d',classes,HERE/'ReferenceModel.java',HERE/'CppGenerationOracle.java'])
        if result.returncode:raise SystemExit(result.stderr)
        for name in names:
            out=capture/name;out.mkdir();row={'case':name};env=dict(os.environ,CPP_ORACLE_RAW_COMMENTS='1')
            if args.mode=='smoke':
                case=SMOKE/name;ref=cpp_reference(case);should_fail=(case/'input/validationfail.txt').exists()
                row.update(scope='cpp-reference' if ref else 'no-cpp-reference',validation_should_fail=should_fail,
                    input_hashes={f.relative_to(ROOT).as_posix():sha(f) for d in (case/'input',case/'auxiliary') if d.exists() for f in sorted(d.rglob('*')) if f.is_file()})
                jargs=[name,out]
            else:ref=True;should_fail=False;jargs=['--manifest',capture/'inventory'/f'{name}.properties',out]
            jvm=run([java,'-Djava.util.logging.config.file='+str(logging),'-cp',f'{classes}:{LIB}/*','CppGenerationOracle',*jargs],env=env)
            row.update(jvm_exit=jvm.returncode,jvm_stage=(out/'stage.txt').read_text().strip() if (out/'stage.txt').exists() else 'setup')
            if (out/'metadata.json').exists():row['effective']=read(out/'metadata.json')
            if (out/'validation.json').exists():
                row['validation_valid']=read(out/'validation.json')['valid'];row['validation_expectation_match']=row['validation_valid']!=should_fail
            if (out/'manifest.json').exists():row['jvm_source_sets']=read(out/'manifest.json')['files'];row['jvm_files_sha256']=tree(out/'files')
            if jvm.returncode:
                row.update(status='jvm_or_export_failure' if ref else 'observed_jvm_failure',diagnostic=jvm.stderr[-4000:]);rows.append(row);print(name,row['status'],flush=True);continue
            if not ref:
                row['status']='observed_jvm_success';rows.append(row);print(name,row['status'],flush=True);continue
            job=read(out/'job.json');row['job_sha256']=sha(out/'job.json');expected=row['jvm_files_sha256'];sets=row['jvm_source_sets']
            snap=run([native,'generate-cpp','--job',out/'job.json','--templates',TEMPLATES,'--output',out/'snapshot-files'])
            if snap.returncode:row['snapshot']={'status':'failure','diagnostic':snap.stderr[-4000:]}
            else:
                actual=tree(out/'snapshot-files');delta=diff(expected,actual);inv=inventory(snap_inv,[out/'job.json',TEMPLATES],sets,actual)
                row['snapshot']={'status':'match' if not any(delta.values()) and inv['status']=='match' else 'mismatch','diff':delta,'inventory':inv}
            meta=row['effective'];options=dict(job['options']);options['docs_placeholders']=meta['placeholders']
            if meta['strict']:options['strict']=True
            write(out/'native-options.json',dict(options,schema='gluecodium.native-cpp-options',version=1));write(out/'native-request.json',{'main':meta['main'],'aux':meta['aux'],'options':options})
            command=[native,'compile-cpp']
            for path in meta['main']:command+=['--input',path]
            for path in meta['aux']:command+=['--auxinput',path]
            command+=['--templates',TEMPLATES,'--output',out/'lime-files','--options',out/'native-options.json']
            if should_fail:(out/'lime-files').mkdir();(out/'lime-files/sentinel.txt').write_text('existing output must survive\n')
            prior=tree(out/'lime-files');lime=run(command)
            if lime.returncode:
                expected_failure=should_fail and lime.stderr.strip().startswith('strict validation failed:') and tree(out/'lime-files')==prior
                row['lime']={'status':'expected_validation_failure' if expected_failure else 'failure','diagnostic':lime.stderr[-4000:]}
            else:
                actual=tree(out/'lime-files');delta=diff(expected,actual);inv=inventory(lime_inv,[out/'native-request.json',TEMPLATES],sets,actual)
                row['lime']={'status':'match' if not any(delta.values()) and inv['status']=='match' else 'mismatch','diff':delta,'inventory':inv}
            row['status']='match' if row.get('validation_expectation_match') and (row['lime']['status']=='expected_validation_failure' if should_fail else row['snapshot']['status']==row['lime']['status']=='match') else 'failure'
            rows.append(row);print(name,'snapshot='+row['snapshot']['status'],'lime='+row['lime']['status'],flush=True)
    after=identity();report={'profile':'gluecodium.cpp-completion-'+args.mode,'version':1,'native_revision':args.revision,'native_compiler':args.native_compiler,
       'source_identity_before':before,'source_identity_after':after,'source_identity_unchanged':before==after,
       'java_version':run([java,'-version']).stderr.strip(),'binaries_sha256':{str(x):sha(x) for x in (native,snap_inv,lime_inv)},'templates_sha256':tree(TEMPLATES),'rows':rows}
    if args.mode=='functional':report['inventory']=read(capture/'inventory/functional-inventory.json')
    write(args.report,report)
    if before!=after or any(r['status'] not in ('match','observed_jvm_success','observed_jvm_failure') for r in rows):raise SystemExit(1)
if __name__=='__main__':main()
