/*
 *

 */
#include "smoke/MethodOverloads.h"
#include "CppProxyBase.h"
#include "FieldAccessMethods.h"
#include "JniBase.h"
#include "JniCppConversionUtils.h"
#include "com_example_smoke_MethodOverloads.h"
#include "ArrayConversionUtils.h"
#include "EnumConversion.h"
#include "EnumSetConversion.h"
#include "InstanceConversion.h"
#include "StructConversion.h"
#include "ProxyConversion.h"
#include "JniReference.h"
extern "C" {
jboolean
Java_com_example_smoke_MethodOverloads_isBoolean__Z(JNIEnv* _jenv, jobject _jinstance, jboolean jinput)
{
    bool input = jinput;
    auto pInstanceSharedPointer = reinterpret_cast<std::shared_ptr<::smoke::MethodOverloads>*> (
        ::genium::jni::get_field_value(
            _jenv,
            ::genium::jni::make_non_releasing_ref(_jinstance),
            "nativeHandle",
            (int64_t*)nullptr));
    auto result = (*pInstanceSharedPointer)->is_boolean(input);
    return result;
}
jboolean
Java_com_example_smoke_MethodOverloads_isBoolean__B(JNIEnv* _jenv, jobject _jinstance, jbyte jinput)
{
    int8_t input = jinput;
    auto pInstanceSharedPointer = reinterpret_cast<std::shared_ptr<::smoke::MethodOverloads>*> (
        ::genium::jni::get_field_value(
            _jenv,
            ::genium::jni::make_non_releasing_ref(_jinstance),
            "nativeHandle",
            (int64_t*)nullptr));
    auto result = (*pInstanceSharedPointer)->is_boolean(input);
    return result;
}
jboolean
Java_com_example_smoke_MethodOverloads_isBoolean__Ljava_lang_String_2(JNIEnv* _jenv, jobject _jinstance, jstring jinput)
{
    ::std::string input = ::genium::jni::convert_from_jni(_jenv,
            ::genium::jni::make_non_releasing_ref(jinput),
            (::std::string*)nullptr);
    auto pInstanceSharedPointer = reinterpret_cast<std::shared_ptr<::smoke::MethodOverloads>*> (
        ::genium::jni::get_field_value(
            _jenv,
            ::genium::jni::make_non_releasing_ref(_jinstance),
            "nativeHandle",
            (int64_t*)nullptr));
    auto result = (*pInstanceSharedPointer)->is_boolean(input);
    return result;
}
jboolean
Java_com_example_smoke_MethodOverloads_isBoolean__Lcom_example_smoke_MethodOverloads_00024Point_2(JNIEnv* _jenv, jobject _jinstance, jobject jinput)
{
    ::smoke::MethodOverloads::Point input = ::genium::jni::convert_from_jni(_jenv,
            ::genium::jni::make_non_releasing_ref(jinput),
            (::smoke::MethodOverloads::Point*)nullptr);
    auto pInstanceSharedPointer = reinterpret_cast<std::shared_ptr<::smoke::MethodOverloads>*> (
        ::genium::jni::get_field_value(
            _jenv,
            ::genium::jni::make_non_releasing_ref(_jinstance),
            "nativeHandle",
            (int64_t*)nullptr));
    auto result = (*pInstanceSharedPointer)->is_boolean(input);
    return result;
}
jboolean
Java_com_example_smoke_MethodOverloads_isBoolean__ZBLjava_lang_String_2Lcom_example_smoke_MethodOverloads_00024Point_2(JNIEnv* _jenv, jobject _jinstance, jboolean jinput1, jbyte jinput2, jstring jinput3, jobject jinput4)
{
    bool input1 = jinput1;
    int8_t input2 = jinput2;
    ::std::string input3 = ::genium::jni::convert_from_jni(_jenv,
            ::genium::jni::make_non_releasing_ref(jinput3),
            (::std::string*)nullptr);
    ::smoke::MethodOverloads::Point input4 = ::genium::jni::convert_from_jni(_jenv,
            ::genium::jni::make_non_releasing_ref(jinput4),
            (::smoke::MethodOverloads::Point*)nullptr);
    auto pInstanceSharedPointer = reinterpret_cast<std::shared_ptr<::smoke::MethodOverloads>*> (
        ::genium::jni::get_field_value(
            _jenv,
            ::genium::jni::make_non_releasing_ref(_jinstance),
            "nativeHandle",
            (int64_t*)nullptr));
    auto result = (*pInstanceSharedPointer)->is_boolean(input1,input2,input3,input4);
    return result;
}
jboolean
Java_com_example_smoke_MethodOverloads_isBooleanStringArrayOverload(JNIEnv* _jenv, jobject _jinstance, jobject jinput)
{
    ::smoke::MethodOverloads::StringArray input = ::genium::jni::convert_from_jni(_jenv,
            ::genium::jni::make_non_releasing_ref(jinput),
            (::smoke::MethodOverloads::StringArray*)nullptr);
    auto pInstanceSharedPointer = reinterpret_cast<std::shared_ptr<::smoke::MethodOverloads>*> (
        ::genium::jni::get_field_value(
            _jenv,
            ::genium::jni::make_non_releasing_ref(_jinstance),
            "nativeHandle",
            (int64_t*)nullptr));
    auto result = (*pInstanceSharedPointer)->is_boolean(input);
    return result;
}
jboolean
Java_com_example_smoke_MethodOverloads_isBooleanIntArrayOverload(JNIEnv* _jenv, jobject _jinstance, jobject jinput)
{
    ::smoke::MethodOverloads::IntArray input = ::genium::jni::convert_from_jni(_jenv,
            ::genium::jni::make_non_releasing_ref(jinput),
            (::smoke::MethodOverloads::IntArray*)nullptr);
    auto pInstanceSharedPointer = reinterpret_cast<std::shared_ptr<::smoke::MethodOverloads>*> (
        ::genium::jni::get_field_value(
            _jenv,
            ::genium::jni::make_non_releasing_ref(_jinstance),
            "nativeHandle",
            (int64_t*)nullptr));
    auto result = (*pInstanceSharedPointer)->is_boolean(input);
    return result;
}
jboolean
Java_com_example_smoke_MethodOverloads_isBoolean__(JNIEnv* _jenv, jobject _jinstance)
{
    auto pInstanceSharedPointer = reinterpret_cast<std::shared_ptr<::smoke::MethodOverloads>*> (
        ::genium::jni::get_field_value(
            _jenv,
            ::genium::jni::make_non_releasing_ref(_jinstance),
            "nativeHandle",
            (int64_t*)nullptr));
    auto result = (*pInstanceSharedPointer)->is_boolean();
    return result;
}
jboolean
Java_com_example_smoke_MethodOverloads_isFloat__Ljava_lang_String_2(JNIEnv* _jenv, jobject _jinstance, jstring jinput)
{
    ::std::string input = ::genium::jni::convert_from_jni(_jenv,
            ::genium::jni::make_non_releasing_ref(jinput),
            (::std::string*)nullptr);
    auto pInstanceSharedPointer = reinterpret_cast<std::shared_ptr<::smoke::MethodOverloads>*> (
        ::genium::jni::get_field_value(
            _jenv,
            ::genium::jni::make_non_releasing_ref(_jinstance),
            "nativeHandle",
            (int64_t*)nullptr));
    auto result = (*pInstanceSharedPointer)->is_float(input);
    return result;
}
jboolean
Java_com_example_smoke_MethodOverloads_isFloat__Ljava_util_List_2(JNIEnv* _jenv, jobject _jinstance, jobject jinput)
{
    ::smoke::MethodOverloads::IntArray input = ::genium::jni::convert_from_jni(_jenv,
            ::genium::jni::make_non_releasing_ref(jinput),
            (::smoke::MethodOverloads::IntArray*)nullptr);
    auto pInstanceSharedPointer = reinterpret_cast<std::shared_ptr<::smoke::MethodOverloads>*> (
        ::genium::jni::get_field_value(
            _jenv,
            ::genium::jni::make_non_releasing_ref(_jinstance),
            "nativeHandle",
            (int64_t*)nullptr));
    auto result = (*pInstanceSharedPointer)->is_float(input);
    return result;
}
JNIEXPORT void JNICALL
Java_com_example_smoke_MethodOverloads_disposeNativeHandle(JNIEnv* _jenv, jobject _jinstance, jlong _jpointerRef)
{
    delete reinterpret_cast<std::shared_ptr<::smoke::MethodOverloads>*> (_jpointerRef);
}
}
