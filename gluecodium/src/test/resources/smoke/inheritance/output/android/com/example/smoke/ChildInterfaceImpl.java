/*
 *
 */
package com.example.smoke;
import android.support.annotation.NonNull;
import com.example.NativeBase;
class ChildInterfaceImpl extends NativeBase implements ChildInterface {
    protected ChildInterfaceImpl(final long nativeHandle, final Object dummy) {
        super(nativeHandle, new Disposer() {
            @Override
            public void disposeNative(long handle) {
                disposeNativeHandle(handle);
            }
        });
    }
    private static native void disposeNativeHandle(long nativeHandle);
    public native void childMethod();
    @Override
    public native void rootMethod();
    @NonNull
    @Override
    public native String getRootProperty();
    @Override
    public native void setRootProperty(@NonNull final String value);
}
