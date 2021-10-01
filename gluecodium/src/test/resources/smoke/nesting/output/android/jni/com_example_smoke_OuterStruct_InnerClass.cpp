/*
 *
 */
#include "com_example_smoke_OuterStruct_InnerClass.h"
#include "com_example_smoke_OuterStruct_InnerClass__Conversion.h"
#include "ArrayConversionUtils.h"
#include "JniClassCache.h"
#include "JniReference.h"
#include "JniWrapperCache.h"
extern "C" {
jobject
Java_com_example_smoke_OuterStruct_00024InnerClass_fooBar(JNIEnv* _jenv, jobject _jinstance)
{
    auto pInstanceSharedPointer = reinterpret_cast<std::shared_ptr<::smoke::OuterStruct::InnerClass>*> (
        ::gluecodium::jni::get_field_value(
            _jenv,
            ::gluecodium::jni::make_non_releasing_ref(_jinstance),
            "nativeHandle",
            (int64_t*)nullptr));
    auto _result = (*pInstanceSharedPointer)->foo_bar();
    return ::gluecodium::jni::convert_to_jni(_jenv, _result).release();
}
JNIEXPORT void JNICALL
Java_com_example_smoke_OuterStruct_00024InnerClass_disposeNativeHandle(JNIEnv* _jenv, jobject _jinstance, jlong _jpointerRef)
{
    auto p_nobj = reinterpret_cast<std::shared_ptr<::smoke::OuterStruct::InnerClass>*>(_jpointerRef);
    ::gluecodium::jni::JniWrapperCache::remove_cached_wrapper(_jenv, *p_nobj);
    delete p_nobj;
}
}
