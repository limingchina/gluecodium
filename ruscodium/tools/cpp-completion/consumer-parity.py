#!/usr/bin/env python3
"""Verify known upstream strict failures and separately passing runtime parity."""
import argparse, hashlib, json, sys
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
FLAGS=['reorder','unused-parameter','sign-compare','unused-result','unused-variable']
def read(p):return json.loads(Path(p).read_text())
def normalized(text,generated,build):
    # Only the generated and build roots vary between the two runs.
    for old,new in sorted(((str(generated.resolve()),'@GENERATED@'),(str(build.resolve()),'@BUILD@')),key=lambda x:-len(x[0])):text=text.replace(old,new)
    return text
def canonical(text):return text.replace(str(ROOT),'@REPO@')
def require(condition,message):
    if not condition:raise ValueError(message)
def rows(report,generated,build):
    result={}
    for x in report['compilations']:
        name=normalized(x['source'],generated,build)
        require(name not in result,'duplicate translation unit '+name)
        result[name]={'exit':x['exit'],'stdout':normalized(x['stdout'],generated,build),'stderr':normalized(x['stderr'],generated,build),
          'command':[normalized(arg,generated,build) for arg in x['command']],'source_sha256':x['source_sha256'],'kind':x['kind'],'index':x['index']}
    return result
def common(a,b,gen_a,gen_b,build_a,build_b,expected_count):
    require(a['planned_translation_units']==b['planned_translation_units']==expected_count,'translation-unit count differs')
    require(len(a['compilations'])==len(b['compilations'])==expected_count,'incomplete translation-unit results')
    require(a['compiler_sha256']==b['compiler_sha256'] and a['compiler']==b['compiler'],'compiler identity differs')
    require(a['gtest_commit']==b['gtest_commit'],'GoogleTest identity differs')
    require(a['generated_sha256']==b['generated_sha256'],'generated paths or bytes differ')
    x,y=rows(a,gen_a,build_a),rows(b,gen_b,build_b)
    require(x.keys()==y.keys(),'translation-unit inventories differ')
    for name in x:require(x[name]==y[name],'compiler result differs: '+name)
    require(sum(v['kind']=='test' for v in x.values())==10,'ten upstream test sources not compiled')
    return x
def verify_compile_flags(entries,compatibility):
    required={'-std=c++17','-Wall','-Wextra','-Werror','-pthread','-DTEST_CPP_VERSION=Cxx17'}
    for name,entry in entries.items():
        command=entry['command'];require(required.issubset(command),'missing strict compiler flags: '+name)
        actual=[arg for arg in command if arg.startswith('-Wno-error=')]
        require(actual==([f'-Wno-error={flag}' for flag in FLAGS] if compatibility else []),'unexpected warning exceptions: '+name)
        includes=[command[i+1] for i,arg in enumerate(command[:-1]) if arg=='-include']
        require(includes==(['cstdint'] if compatibility else []),'unexpected forced includes: '+name)
def verify_strict(a,b,gen_a,gen_b,build_a,build_b,catalog):
    require(a['strict'] and b['strict'] and not a['complete'] and not b['complete'],'strict failure reports required')
    require(a['compiler_sha256']==catalog['compiler_sha256'] and a['compiler']['stdout']==catalog['compiler_version'],'compiler differs from strict upstream catalog')
    require(not a['upstream_warning_exceptions'] and not b['upstream_warning_exceptions'] and not a['upstream_include_exceptions'] and not b['upstream_include_exceptions'],'strict report has exceptions')
    entries=common(a,b,gen_a,gen_b,build_a,build_b,catalog['translation_units'])
    verify_compile_flags(entries,False)
    tree_hash=hashlib.sha256(json.dumps(a['generated_sha256'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    require(tree_hash==catalog['evidence']['generated_file_hashes_sha256'],'generated files differ from strict JVM baseline')
    failures={canonical(name):[canonical(line) for line in x['stderr'].splitlines() if ': error:' in line] for name,x in entries.items() if x['exit']}
    require(failures==catalog['failures'],'strict failures differ from known upstream source/location/message catalog')
    return {'translation_units':len(entries),'known_failing_units':len(failures),'strict_passed':False,'diagnostic_parity':True}
def xml_cases(path):
    root=ET.parse(path).getroot();result=[]
    for suite in root.iter('testsuite'):
        for case in suite.findall('testcase'):
            source=Path(case.get('file','')).resolve().relative_to(ROOT.resolve()).as_posix()
            result.append((suite.get('name'),case.get('name'),source,int(case.get('line','0')),case.get('status'),case.get('result'),len(case.findall('failure')),len(case.findall('skipped'))))
    return sorted(result)
def listed_tests(output):
    suite=None;result=[]
    for line in output.splitlines():
        line=line.split('  #',1)[0].rstrip()
        if line and not line[0].isspace() and line.endswith('.'):suite=line[:-1]
        elif line.startswith('  ') and suite:result.append((suite,line.strip()))
    return sorted(result)
def verify_compat(a,b,gen_a,gen_b,build_a,build_b,count):
    for report in (a,b):
        require(not report['strict'] and report['complete'],'compatibility run incomplete')
        require(report['upstream_warning_exceptions']==FLAGS and report['upstream_include_exceptions']==['cstdint'],'compatibility exceptions differ')
        require(report['link']['exit']==report['run']['exit']==0,'compatibility link or test run failed')
        require(report.get('gtest_environment_sanitized') is True and report.get('gtest_inventory_match') is True,'unfiltered GTest inventory not verified')
        require('--gtest_filter=*' in report['run']['command'] and '--gtest_filter=*' in report['gtest_list']['command'] and '--gtest_list_tests' in report['gtest_list']['command'] and report['gtest_list']['exit']==0,'GTest unfiltered commands missing')
    entries=common(a,b,gen_a,gen_b,build_a,build_b,count)
    verify_compile_flags(entries,True)
    require(all(not x['exit'] for x in entries.values()),'compatibility compilation failed')
    la,lb=a['link'],b['link']
    for key in ('command','stdout','stderr'):
        xa=la[key];xb=lb[key]
        if isinstance(xa,list):xa=[normalized(t,gen_a,build_a) for t in xa];xb=[normalized(t,gen_b,build_b) for t in xb]
        else:xa=normalized(xa,gen_a,build_a);xb=normalized(xb,gen_b,build_b)
        require(xa==xb,'link '+key+' differs')
    expected=read(HERE/'gtest-inventory.json')['cases']
    names=sorted((x['suite'],x['name']) for x in expected)
    require(len(expected)==216 and listed_tests(a['gtest_list']['stdout'])==listed_tests(b['gtest_list']['stdout'])==names,'GTest listed inventory differs from baseline')
    for report,build in ((a,build_a),(b,build_b)):
        require(hashlib.sha256((build/'tests.xml').read_bytes()).hexdigest()==report['gtest_xml_sha256'],'GTest XML hash differs from report')
    xa,xb=xml_cases(build_a/'tests.xml'),xml_cases(build_b/'tests.xml')
    wanted=sorted((x['suite'],x['name'],x['file'],x['line'],'run','completed',0,0) for x in expected)
    require(xa==xb==wanted,'GTest case inventories or outcomes differ from baseline')
    require(a.get('gtest_tests')==b.get('gtest_tests')==len(xa)==216,'GTest test counts differ')
    require(a.get('gtest_failures')==b.get('gtest_failures')==0,'GTest failures')
    return {'translation_units':len(entries),'test_sources':10,'gtest_cases':len(xa),'runtime_parity':True,'warning_exceptions':FLAGS,'include_exceptions':['cstdint']}
def verify_names(a,b,gen_a,gen_b,build_a,build_b):
    for report in (a,b):
        require(report['status']=='compile_failure' and report['compile_exit']!=0,'naming strict failure required')
        require(report.get('compatibility_compile_exit')==0 and report.get('compatibility_run_exit')==0,'naming compatibility run failed')
    require(a['compiler_version']==b['compiler_version'],'naming compiler differs')
    for key in ('compile_command','compile_stdout','compile_stderr','compatibility_compile_command','compatibility_compile_stderr','compatibility_run_stderr'):
        x,y=a.get(key,''),b.get(key,'')
        if isinstance(x,list):x=[normalized(v,gen_a,build_a) for v in x];y=[normalized(v,gen_b,build_b) for v in y]
        else:x=normalized(x,gen_a,build_a);y=normalized(y,gen_b,build_b)
        require(x==y,'naming result differs: '+key)
    errors=[line for line in a['compile_stderr'].splitlines() if ': error:' in line]
    require(len(errors)==1 and 'NameRulesImpl.cpp:26:125: error:' in errors[0] and '[-Werror=unused-parameter]' in errors[0], 'unexpected naming strict diagnostic')
    def source_hashes(report,gen,build):return {normalized(k,gen,build):v for k,v in report['source_sha256'].items()}
    require(source_hashes(a,gen_a,build_a)==source_hashes(b,gen_b,build_b),'naming source hashes differ')
    return {'strict_passed':False,'diagnostic_parity':True,'compatibility_runtime_passed':True}
def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('functional-report','jvm-strict','native-strict','jvm-compat','native-compat','jvm-generated','native-generated','jvm-names','native-names','jvm-names-generated','native-names-generated','report'):p.add_argument('--'+name,required=True,type=Path)
    p.add_argument('--catalog',type=Path,default=HERE/'strict-known-diagnostics.json');args=p.parse_args();result={'profile':'gluecodium.cpp-consumer-parity','strict_passed':False,'status':'failure'}
    try:
        oracle=read(args.functional_report);case=next(x for x in oracle['rows'] if x['case']=='functional')
        require(oracle['source_identity_unchanged'] and case['snapshot']['status']==case['lime']['status']=='match','full generated byte/source-set parity required')
        catalog=read(args.catalog);j,n=read(args.jvm_strict),read(args.native_strict)
        result['strict']=verify_strict(j,n,args.jvm_generated,args.native_generated,args.jvm_strict.parent,args.native_strict.parent,catalog)
        j,n=read(args.jvm_compat),read(args.native_compat)
        result['compatibility']=verify_compat(j,n,args.jvm_generated,args.native_generated,args.jvm_compat.parent,args.native_compat.parent,catalog['translation_units'])
        names=next(x for x in oracle['rows'] if x['case']=='namerules')
        require(names['snapshot']['status']==names['lime']['status']=='match','naming generated byte/source-set parity required')
        result['naming']=verify_names(read(args.jvm_names),read(args.native_names),args.jvm_names_generated,args.native_names_generated,args.jvm_names.parent,args.native_names.parent)
        result['status']='expected_upstream_failure_parity_and_runtime_match'
    except (ValueError,KeyError,StopIteration,OSError,ET.ParseError) as error:result['diagnostic']=str(error)
    args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],result.get('diagnostic',''),flush=True)
    if result['status']=='failure':sys.exit(1)
if __name__=='__main__':main()
