/*
 *

 */
package com.example.examples;
import android.support.annotation.NonNull;
import com.example.NativeBase;
public final class BuiltinTypes extends NativeBase {
    /**
     * For internal use only.
     * @exclude
     */
    protected BuiltinTypes(final long nativeHandle) {
        super(nativeHandle, new Disposer() {
            @Override
            public void disposeNative(long handle) {
                disposeNativeHandle(handle);
            }
        });
    }
    private static native void disposeNativeHandle(long nativeHandle);
    public static native short methodWithUInt8(final short inputNumber);
    public static native int methodWithInt32(final int inputNumber);
    public static native long methodWithUInt64(final long inputNumber);
    public static native boolean methodWithBoolean(final boolean inputCondition);
    public static native double methodWithDouble(final double inputNumber);
    @NonNull
    public static native String methodWithString(@NonNull final String inputString);
    @NonNull
    public static native byte[] methodWithByteBuffer(@NonNull final byte[] inputBuffer);
}