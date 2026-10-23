/*

 *
 */

@file:JvmName("OnlyFunctionsExtensions")


package com.example.smoke

import com.example.NativeBase

/**
 * Cpp is included for methods that need a native implementation.
 */
class OnlyFunctions : NativeBase {



    /**
     * For internal use only.
     * @suppress
     * @param nativeHandle The handle to resources on C++ side.
     * @param tag Tag used by callers to avoid overload resolution problems.
     */
    protected constructor(nativeHandle: Long, @Suppress("UNUSED_PARAMETER") tag: Any?)
        : super(nativeHandle, { disposeNativeHandle(it) }) {}







    companion object {
        @JvmField final val KOTLIN_CONSTANT: Int = 22
        @JvmStatic private external fun disposeNativeHandle(nativeHandle: Long)
        /**
         *
         * @param input String to round trip through the native implementation.
         * @return The unchanged input.
         */

        @JvmStatic external fun kotlinOnly(input: String) : String
        /**
         *
         * @param input String to round trip through the native implementation.
         * @return The unchanged input.
         */

        @JvmStatic external fun shared(input: String) : String
    }
}
