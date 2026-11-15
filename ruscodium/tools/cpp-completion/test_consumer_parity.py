import copy
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
                    'command':['c++','-std=c++17','-c',str(path),'-o',str(build/f'{i}.o')]})
            return {'strict':True,'complete':False,'compiler_sha256':'same','compiler':{'stdout':'GCC 14'},'gtest_commit':'pin',
              'generated_sha256':{'0.cpp':'abc'},'planned_translation_units':11,'compilations':rows,'upstream_warning_exceptions':[],'upstream_include_exceptions':[]}
        self.a=report(self.gen_a,self.build_a);self.b=report(self.gen_b,self.build_b)
        self.catalog={'translation_units':11,'compiler_sha256':'same','compiler_version':'GCC 14',
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

if __name__=='__main__':unittest.main()
