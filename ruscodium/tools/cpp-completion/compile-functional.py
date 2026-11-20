#!/usr/bin/env python3
"""Compile every generated and upstream functional C++ unit and run all GTests."""
import argparse, concurrent.futures, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[3]
GTEST_COMMIT='6910c9d9165801d8827d628cb72eb7ea9dd538c5'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def tree(path):return {p.relative_to(path).as_posix():digest(p) for p in sorted(path.rglob('*')) if p.is_file()}
def command(args,env=None):
 a=[str(x) for x in args];p=subprocess.run(a,cwd=ROOT,text=True,capture_output=True,env=env)
 return {'command':a,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def source_inventory(inventory):
 features=inventory.get('features',[]);tests=inventory.get('test_sources',[])
 if len(features)!=45 or len(tests)!=10:raise ValueError('expected 45 feature groups and 10 test source files')
 handwritten=sorted({ROOT/p for feature in features for p in feature['cpp'] if p.endswith('.cpp')})
 tests=sorted(ROOT/p for p in tests)
 if len(handwritten)!=92:raise ValueError(f'expected 92 handwritten C++ sources, found {len(handwritten)}')
 hashes=inventory.get('hashes',{})
 header_paths=sorted({ROOT/p for feature in features for p in feature['cpp'] if p.endswith('.h')})+[ROOT/p for p in inventory.get('test_headers',[])]
 for path in handwritten+tests+header_paths:
  if not path.is_file() or not path.resolve().is_relative_to(ROOT.resolve()):raise ValueError(f'missing or unsafe source: {path}')
  if hashes.get(path.relative_to(ROOT).as_posix())!=digest(path):raise ValueError(f'source changed since inventory: {path}')
 return handwritten,tests
def compile_all(tasks,jobs,collect):
 results=[];failed=False
 with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
  # Bounded scheduling permits the strict gate to stop early while the explicit
  # diagnostic mode compiles all units and records all failures.
  iterator=iter(tasks);running={}
  def submit():
   try: task=next(iterator)
   except StopIteration:return False
   future=pool.submit(command,task['command']);running[future]=task;return True
  for _ in range(jobs):submit()
  while running:
   done,_=concurrent.futures.wait(running,return_when=concurrent.futures.FIRST_COMPLETED)
   for future in done:
    task=running.pop(future);result=future.result();result.update(source=str(task['source']),source_sha256=digest(task['source']),kind=task['kind'],index=task['index']);results.append(result)
    if result['exit']:failed=True
    if len(results)%20==0:print(f'compiled {len(results)}/{len(tasks)} translation units',flush=True)
   if collect or not failed:
    while len(running)<jobs and submit():pass
 return sorted(results,key=lambda x:x['index'])
def sanitized_gtest_env(env):return {k:v for k,v in env.items() if not k.startswith('GTEST_')}
def listed_tests(output):
 suite=None;result=[]
 for line in output.splitlines():
  line=line.split('  #',1)[0].rstrip()
  if line and not line[0].isspace() and line.endswith('.'):suite=line[:-1]
  elif line.startswith('  ') and suite:result.append((suite,line.strip()))
 return sorted(result)
def xml_inventory(path):
 root=ET.parse(path).getroot();cases=[]
 for suite in root.iter('testsuite'):
  for case in suite.findall('testcase'):
   file=Path(case.get('file','')).resolve().relative_to(ROOT.resolve()).as_posix()
   cases.append({'suite':suite.get('name'),'name':case.get('name'),'file':file,'line':int(case.get('line','0'))})
   if case.get('status')!='run' or case.get('result')!='completed' or case.findall('failure') or case.findall('skipped'):
    raise ValueError('GTest case did not complete successfully')
 return sorted(cases,key=lambda x:(x['suite'],x['name']))
def main():
 p=argparse.ArgumentParser(description=__doc__)
 for name in ('inventory','generated','expected-inventory','gtest-source','output'):p.add_argument('--'+name,required=True,type=Path)
 p.add_argument('--label',required=True);p.add_argument('--compiler',default=os.environ.get('CXX','c++'));p.add_argument('--jobs',type=int,default=2)
 p.add_argument('--upstream-warning',action='append',default=[],choices=('reorder','unused-parameter','sign-compare','unused-result','unused-variable'))
 p.add_argument('--upstream-include',action='append',default=[],choices=('cstdint',));p.add_argument('--collect-errors',action='store_true');args=p.parse_args()
 if args.jobs<1:p.error('--jobs must be positive')
 generated=args.generated.resolve();gtest=args.gtest_source.resolve();compiler=shutil.which(args.compiler)
 if compiler is None:p.error('C++ compiler is unavailable')
 inv=json.loads(args.inventory.read_text())
 try: handwritten,tests=source_inventory(inv)
 except ValueError as e:p.error(str(e))
 expected=json.loads(args.expected_inventory.read_text())['files'];generated_hashes=tree(generated)
 if set(expected)!=set(generated_hashes):p.error('generated tree differs from complete JVM path inventory')
 if set(expected.values())!={'MAIN','COMMON'}:p.error('source-set inventory must contain MAIN and COMMON')
 version=command(['git','-C',gtest,'rev-parse','HEAD']);clean=command(['git','-C',gtest,'status','--porcelain'])
 if version['exit'] or version['stdout'].strip()!=GTEST_COMMIT or clean['exit'] or clean['stdout']:p.error('GoogleTest checkout must be clean upstream v1.16.0 at pinned commit')
 args.output.mkdir(parents=True,exist_ok=False);report_path=args.output/'report.json'
 cpp_root=ROOT/'functional-tests/functional/input/src/cpp'
 common=[compiler,'-std=c++17','-Wall','-Wextra','-Werror','-pthread','-DTEST_CPP_VERSION=Cxx17','-I',generated/'cpp/include','-I',cpp_root,'-I',cpp_root/'include','-isystem',gtest/'googletest/include','-isystem',gtest/'googlemock/include','-I',gtest/'googletest','-I',gtest/'googlemock']
 common += [f'-Wno-error={warning}' for warning in args.upstream_warning]
 for header in args.upstream_include:common+=['-include',header]
 sources=[(x,'generated') for x in sorted((generated/'cpp/src').rglob('*.cpp'))]
 if not sources:p.error('no generated implementations')
 sources += [(x,'handwritten') for x in handwritten]+[(x,'test') for x in tests]
 sources += [(gtest/x,'test-framework') for x in ('googletest/src/gtest-all.cc','googlemock/src/gmock-all.cc','googlemock/src/gmock_main.cc')]
 tasks=[{'source':src,'kind':kind,'index':i,'command':common+['-c',src,'-o',args.output/f'{i:04}.o']} for i,(src,kind) in enumerate(sources)]
 report={'schema':'gluecodium.cpp-functional-build','version':1,'label':args.label,'compiler':command([compiler,'--version']),
  'compiler_sha256':digest(Path(compiler)),'inventory_sha256':digest(args.inventory),'expected_inventory_sha256':digest(args.expected_inventory),
  'generated_sha256':generated_hashes,'gtest_commit':GTEST_COMMIT,'planned_translation_units':len(tasks),
  'strict':not(args.upstream_warning or args.upstream_include),'upstream_warning_exceptions':args.upstream_warning,
  'upstream_include_exceptions':args.upstream_include,'collect_errors':args.collect_errors,'compilations':[],'complete':False}
 try:
  report['compilations']=compile_all(tasks,args.jobs,args.collect_errors)
  for entry in report['compilations']:
   if entry['exit']:print('compile failed:',entry['source'],entry['stderr'],file=sys.stderr,flush=True)
  if len(report['compilations'])!=len(tasks) or any(x['exit'] for x in report['compilations']):return 1
  exe=args.output/'functional-tests';report['link']=command([compiler,'-pthread',*[args.output/f'{i:04}.o' for i in range(len(tasks))],'-o',exe])
  if report['link']['exit']:print(report['link']['stderr'],file=sys.stderr);return 1
  clean_env=sanitized_gtest_env(os.environ);report['gtest_environment_sanitized']=True
  expected_cases=json.loads((Path(__file__).parent/'gtest-inventory.json').read_text())['cases']
  report['gtest_list']=command([exe,'--gtest_filter=*','--gtest_list_tests'],env=clean_env)
  expected_names=sorted((x['suite'],x['name']) for x in expected_cases)
  if report['gtest_list']['exit'] or listed_tests(report['gtest_list']['stdout'])!=expected_names:
   report['gtest_inventory_error']='GTest list differs from 216-case upstream inventory';return 1
  xml=args.output/'tests.xml';report['run']=command([exe,'--gtest_filter=*',f'--gtest_output=xml:{xml}'],env=clean_env);print(report['run']['stdout'],end='',flush=True)
  if xml.exists():
   root=ET.parse(xml).getroot();report['gtest_xml_sha256']=digest(xml);report['gtest_tests']=int(root.attrib.get('tests','0'));report['gtest_failures']=int(root.attrib.get('failures','0'))
   try:report['gtest_inventory_match']=xml_inventory(xml)==expected_cases
   except (ValueError,TypeError):report['gtest_inventory_match']=False
  report['complete']=report['run']['exit']==0 and report.get('gtest_tests')==len(expected_cases)==216 and report.get('gtest_failures',-1)==0 and report.get('gtest_inventory_match',False)
  return 0 if report['complete'] else 1
 finally:report_path.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':sys.exit(main())
