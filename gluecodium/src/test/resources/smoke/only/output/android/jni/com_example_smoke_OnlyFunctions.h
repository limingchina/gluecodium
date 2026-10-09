/*

 *
 */

#pragma once

#include <jni.h>

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT jstring JNICALL
Java_com_example_smoke_OnlyFunctions_javaOnly(JNIEnv* _jenv, jobject _jinstance, jstring jinput);
JNIEXPORT jstring JNICALL
Java_com_example_smoke_OnlyFunctions_shared(JNIEnv* _jenv, jobject _jinstance, jstring jinput);



#ifdef __cplusplus
}
#endif
