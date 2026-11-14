#!/usr/bin/env python3
"""Compile and run the upstream naming implementation with generated C++17."""
import argparse, hashlib, json, os, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--generated',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--label',required=True);args=p.parse_args();out=args.output.resolve();generated=args.generated.resolve()
 if out.exists() and any(out.iterdir()):raise SystemExit('output must be empty')
 out.mkdir(parents=True,exist_ok=True);sources=sorted((generated/'cpp/src').rglob('*.cpp'));handwritten=ROOT/'functional-tests/namerules/cpp/NameRulesImpl.cpp';consumer=HERE/'fixtures/namerules-consumer.cc';include=generated/'cpp/include';report={'label':args.label,'compiler':os.environ.get('CXX','c++')}
 if not sources or not include.is_dir():report.update(status='missing_generated_sources');(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');raise SystemExit(1)
 version=subprocess.run([report['compiler'],'--version'],capture_output=True,text=True);report['compiler_version']=version.stdout.splitlines()[0] if version.stdout else version.stderr
 inputs=sources+[handwritten,consumer];report['source_sha256']={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in inputs}
 command=[report['compiler'],'-std=c++17','-Wall','-Wextra','-Werror','-I',str(include),*[str(x) for x in inputs],'-o',str(out/'consumer')];report['compile_command']=command
 result=subprocess.run(command,capture_output=True,text=True,cwd=ROOT);report.update(compile_exit=result.returncode,compile_stdout=result.stdout,compile_stderr=result.stderr)
 if result.returncode:
  report['status']='compile_failure'
  if 'NameRulesImpl.cpp' in result.stderr and '[-Werror=unused-parameter]' in result.stderr:
   fallback=command[:4]+['-Wno-error=unused-parameter']+command[4:];relaxed=subprocess.run(fallback,capture_output=True,text=True,cwd=ROOT)
   report.update(compatibility_compile_command=fallback,compatibility_compile_exit=relaxed.returncode,compatibility_compile_stderr=relaxed.stderr)
   if not relaxed.returncode:
    run_result=subprocess.run([str(out/'consumer')],capture_output=True,text=True,cwd=ROOT);report.update(compatibility_run_exit=run_result.returncode,compatibility_run_stderr=run_result.stderr)
 else:
  result=subprocess.run([str(out/'consumer')],capture_output=True,text=True,cwd=ROOT);report.update(run_exit=result.returncode,run_stdout=result.stdout,run_stderr=result.stderr,status='match' if result.returncode==0 else 'run_failure')
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(args.label,report['status'],flush=True)
 if report['status']!='match':raise SystemExit(1)
if __name__=='__main__':main()
