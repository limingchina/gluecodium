/*
 *

 */
package com.example.smoke;
public final class ChildClassFromInterface extends ParentInterfaceImpl {
    /**
     * For internal use only.
     * @exclude
     */
    protected ChildClassFromInterface(final long nativeHandle) {
        super(nativeHandle);
    }
    public native void childClassMethod();
}
