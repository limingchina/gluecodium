import copy
import hashlib
import json
import importlib.util
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('consumer_parity',HERE/'consumer-parity.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class StrictParityTests(unittest.TestCase):
    def setUp(self):
        self.gen_a=Path('/tmp/jvm-gen');self.gen_b=Path('/tmp/native-gen');self.build_a=Path('/tmp/jvm-build');self.build_b=Path('/tmp/native-build')
        def report(gen,build):
            rows=[]
            for i in range(11):
                path=gen/f'{i}.cpp' if i==0 else Path(f'/workspace/gluecodium/test-{i}.cpp')
                rows.append({'source':str(path),'source_sha256':str(i),'kind':'generated' if i==0 else 'test','index':i,
                    'exit':1 if i==0 else 0,'stdout':'','stderr':f'{path}:4:2: error: bad [-Werror=reorder]\n' if i==0 else '',
                    'command':['c++','-std=c++17','-Wall','-Wextra','-Werror','-pthread','-DTEST_CPP_VERSION=Cxx17','-c',str(path),'-o',str(build/f'{i}.o')]})
            return {'strict':True,'complete':False,'compiler_sha256':'same','compiler':{'stdout':'GCC 14'},'gtest_commit':'pin',
              'generated_sha256':{'0.cpp':'abc'},'planned_translation_units':11,'compilations':rows,'upstream_warning_exceptions':[],'upstream_include_exceptions':[]}
        self.a=report(self.gen_a,self.build_a);self.b=report(self.gen_b,self.build_b)
        self.catalog={'translation_units':11,'compiler_sha256':'same','compiler_version':'GCC 14',
          'evidence':{'generated_file_hashes_sha256':hashlib.sha256(json.dumps(self.a['generated_sha256'],sort_keys=True,separators=(',',':')).encode()).hexdigest()},
          'failures':{'@GENERATED@/0.cpp':['@GENERATED@/0.cpp:4:2: error: bad [-Werror=reorder]']}}
    def verify(self):return m.verify_strict(self.a,self.b,self.gen_a,self.gen_b,self.build_a,self.build_b,self.catalog)
    def test_known_identical_failure_is_not_strict_success(self):
        result=self.verify();self.assertTrue(result['diagnostic_parity']);self.assertFalse(result['strict_passed'])
    def test_changed_message_rejected(self):
        self.b['compilations'][0]['stderr']=self.b['compilations'][0]['stderr'].replace('bad','different')
        with self.assertRaises(ValueError):self.verify()
    def test_symmetric_unknown_diagnostic_rejected(self):
        for report in (self.a,self.b):report['compilations'][0]['stderr']=report['compilations'][0]['stderr'].replace('bad','new failure')
        with self.assertRaises(ValueError):self.verify()
    def test_symmetric_missing_strict_flag_rejected(self):
        for report in (self.a,self.b):report['compilations'][0]['command'].remove('-Werror')
        with self.assertRaises(ValueError):self.verify()
    def test_symmetric_standard_override_rejected(self):
        for report in (self.a,self.b):report['compilations'][0]['command'].append('-std=c++14')
        with self.assertRaises(ValueError):self.verify()
    def test_symmetric_warning_suppression_rejected(self):
        for report in (self.a,self.b):report['compilations'][0]['command'].append('-w')
        with self.assertRaises(ValueError):self.verify()
    def test_uncompiled_unit_rejected(self):
        self.b['compilations'].pop()
        with self.assertRaises(ValueError):self.verify()
    def test_extra_compiler_flag_rejected(self):
        self.b['compilations'][5]['command'].append('-Wno-error')
        with self.assertRaises(ValueError):self.verify()
    def test_known_warning_at_new_location_rejected(self):
        for report in (self.a,self.b):report['compilations'][0]['stderr']=report['compilations'][0]['stderr'].replace(':4:2:', ':5:2:')
        with self.assertRaises(ValueError):self.verify()
    def test_unrelated_path_is_not_normalized(self):
        self.b['compilations'][0]['stderr']=self.b['compilations'][0]['stderr'].replace('bad','bad in /tmp/unrelated')
        with self.assertRaises(ValueError):self.verify()
    def test_different_output_bytes_rejected(self):
        self.b['generated_sha256']['0.cpp']='different'
        with self.assertRaises(ValueError):self.verify()


class RuntimeInventoryTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        import xml.etree.ElementTree as ET
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        base=Path(self.temp.name);self.ga=base/'jvm-gen';self.gb=base/'native-gen';self.ba=base/'jvm-build';self.bb=base/'native-build'
        for p in (self.ga,self.gb,self.ba,self.bb):p.mkdir()
        self.expected=json.loads((HERE/'gtest-inventory.json').read_text())['cases']
        root=ET.Element('testsuites',tests='216',failures='0');suites={}
        for case in self.expected:
            suite=suites.get(case['suite'])
            if suite is None:suite=ET.SubElement(root,'testsuite',name=case['suite']);suites[case['suite']]=suite
            ET.SubElement(suite,'testcase',name=case['name'],file=str(m.ROOT/case['file']),line=str(case['line']),status='run',result='completed')
        for build in (self.ba,self.bb):ET.ElementTree(root).write(build/'tests.xml',encoding='utf-8',xml_declaration=True)
        listing='';last=None
        for case in self.expected:
            if case['suite']!=last:listing+=case['suite']+'.\n';last=case['suite']
            listing+='  '+case['name']+'\n'
        def report(gen,build):
            rows=[]
            for i in range(11):
                src=gen/f'{i}.cpp' if i==0 else m.ROOT/f'test-{i}.cpp'
                rows.append({'source':str(src),'source_sha256':str(i),'kind':'generated' if i==0 else 'test','index':i,'exit':0,'stdout':'','stderr':'',
                  'command':['c++','-std=c++17','-Wall','-Wextra','-Werror','-pthread','-DTEST_CPP_VERSION=Cxx17',*[f'-Wno-error={x}' for x in m.FLAGS],'-include','cstdint','-c',str(src),'-o',str(build/f'{i}.o')]})
            return {'strict':False,'complete':True,'upstream_warning_exceptions':m.FLAGS[:],'upstream_include_exceptions':['cstdint'],
              'compiler_sha256':'same','compiler':{'stdout':'GCC 14'},'gtest_commit':'pin','generated_sha256':{'0.cpp':'abc'},
              'planned_translation_units':11,'compilations':rows,'link':{'exit':0,'stdout':'','stderr':'','command':['c++','-o',str(build/'test')]},
              'run':{'exit':0,'command':[str(build/'test'),'--gtest_filter=*']},'gtest_environment_sanitized':True,'gtest_inventory_match':True,
              'gtest_list':{'exit':0,'command':[str(build/'test'),'--gtest_filter=*','--gtest_list_tests'],'stdout':listing},
              'gtest_tests':216,'gtest_failures':0,'gtest_xml_sha256':hashlib.sha256((build/'tests.xml').read_bytes()).hexdigest()}
        self.a=report(self.ga,self.ba);self.b=report(self.gb,self.bb)
    def verify(self):return m.verify_compat(self.a,self.b,self.ga,self.gb,self.ba,self.bb,11)
    def test_complete_inventory_passes(self):self.assertEqual(self.verify()['gtest_cases'],216)
    def test_both_sides_missing_a_test_fail(self):
        for report in (self.a,self.b):report['gtest_list']['stdout']=report['gtest_list']['stdout'].replace('  GettingFieldsOnLvalue\n','')
        with self.assertRaises(ValueError):self.verify()
    def test_symmetric_skipped_test_fails(self):
        import xml.etree.ElementTree as ET
        for report,build in ((self.a,self.ba),(self.b,self.bb)):
            path=build/'tests.xml';doc=ET.parse(path);next(doc.getroot().iter('testcase')).set('result','skipped');doc.write(path,encoding='utf-8',xml_declaration=True)
            report['gtest_xml_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
        with self.assertRaises(ValueError):self.verify()
    def test_forced_test_listing_cannot_hide_filter(self):
        import importlib.util
        source=importlib.util.spec_from_file_location('compile_functional',HERE/'compile-functional.py')
        builder=importlib.util.module_from_spec(source);source.loader.exec_module(builder)
        env=builder.sanitized_gtest_env({'GTEST_FILTER':'A.*','GTEST_TOTAL_SHARDS':'2','GTEST_SHARD_INDEX':'0','PATH':'safe'})
        self.assertEqual(env,{'PATH':'safe'})
    def test_additional_filter_fails(self):
        for report in (self.a,self.b):report['run']['command'].append('--gtest_filter=EnumTest.*')
        with self.assertRaises(ValueError):self.verify()
    def test_unsanitized_environment_fails(self):
        for report in (self.a,self.b):report['gtest_environment_sanitized']=False
        with self.assertRaises(ValueError):self.verify()

if __name__=='__main__':unittest.main()
