/*

 *
 */

package com.example.smoke;

import android.support.annotation.NonNull;
import com.example.NativeBase;

/**
 * <p>Cpp is included for methods that need a native implementation.
 */
public final class OnlyFunctions extends NativeBase {
    public static final int JAVA_CONSTANT = 11;

    /**
     * For internal use only.
     * @hidden
     * @param nativeHandle The SDK nativeHandle instance.
     * @param dummy The SDK dummy instance.
     */
    protected OnlyFunctions(final long nativeHandle, final Object dummy) {
        super(nativeHandle, new Disposer() {
            @Override
            public void disposeNative(long handle) {
                disposeNativeHandle(handle);
            }
        });
    }

    private static native void disposeNativeHandle(long nativeHandle);


    /**
     *
     * @param input <p>String to round trip through the native implementation.
     * @return <p>The unchanged input.
     */
    @NonNull
    public static native String javaOnly(@NonNull final String input);

    /**
     *
     * @param input <p>String to round trip through the native implementation.
     * @return <p>The unchanged input.
     */
    @NonNull
    public static native String shared(@NonNull final String input);



}
