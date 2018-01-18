//
// Copyright (C) 2018 HERE Global B.V. and/or its affiliated companies. All rights reserved.
//
// This software, including documentation, is protected by copyright controlled by
// HERE Global B.V. All rights are reserved. Copying, including reproducing, storing,
// adapting or translating, any or all of this material requires the prior written
// consent of HERE Global B.V. This material also contains confidential information,
// which may not be disclosed to others without prior written consent of HERE Global B.V.
//
// Automatically generated. Do not modify. Your changes will be lost.

import Foundation



internal func getRef(_ ref: InstanceWithStruct) -> RefHolder {
    return RefHolder(ref.c_instance)
}
public class InstanceWithStruct {
    let c_instance : _baseRef

    public init?(cInstanceWithStruct: _baseRef) {
        guard cInstanceWithStruct.private_pointer != nil else {
            return nil
        }
        c_instance = cInstanceWithStruct
    }

    deinit {
        smoke_InstanceWithStruct_release(c_instance)
    }
    public struct InnerStruct {
        public var value: Int8

        public init(value: Int8) {
            self.value = value
        }

        internal init?(cInnerStruct: _baseRef) {
            value = smoke_InstanceWithStruct_InnerStruct_value_get(cInnerStruct)
        }

        internal func convertToCType() -> _baseRef {
            let result = smoke_InstanceWithStruct_InnerStruct_create()
            fillFunction(result)
            return result
        }

        internal func fillFunction(_ cInnerStruct: _baseRef) -> Void {
            smoke_InstanceWithStruct_InnerStruct_value_set(cInnerStruct, value)
        }
    }

    public struct StructWithInstance {
        public var instance: SimpleInstantiableOne

        public init(instance: SimpleInstantiableOne) {
            self.instance = instance
        }

        internal init?(cStructWithInstance: _baseRef) {
            do {
                guard
                    let instanceUnwrapped = SimpleInstantiableOne(cSimpleInstantiableOne: smoke_SimpleInstantiableOne_copy(smoke_InstanceWithStruct_StructWithInstance_instance_get(cStructWithInstance)))
                else {
                    return nil
                }
                instance = instanceUnwrapped
            }
        }

        internal func convertToCType() -> _baseRef {
            let result = smoke_InstanceWithStruct_StructWithInstance_create()
            fillFunction(result)
            return result
        }

        internal func fillFunction(_ cStructWithInstance: _baseRef) -> Void {
            smoke_InstanceWithStruct_StructWithInstance_instance_set(cStructWithInstance, getRef(instance).ref)
        }
    }

    public func innerStructMethod(inputStruct: InstanceWithStruct.InnerStruct) -> InstanceWithStruct.InnerStruct? {
        let inputStructHandle = inputStruct.convertToCType()
        defer {
            smoke_InstanceWithStruct_InnerStruct_release(inputStructHandle)
        }
        let cResult = smoke_InstanceWithStruct_innerStructMethod(c_instance, inputStructHandle)
        defer {
            smoke_InstanceWithStruct_InnerStruct_release(cResult)
        }
        return InstanceWithStruct.InnerStruct(cInnerStruct: cResult)
    }

    public func structWithInstanceMethod(input: InstanceWithStruct.StructWithInstance) -> InstanceWithStruct.StructWithInstance? {
        let inputHandle = input.convertToCType()
        defer {
            smoke_InstanceWithStruct_StructWithInstance_release(inputHandle)
        }
        let cResult = smoke_InstanceWithStruct_structWithInstanceMethod(c_instance, inputHandle)
        defer {
            smoke_InstanceWithStruct_StructWithInstance_release(cResult)
        }
        return InstanceWithStruct.StructWithInstance(cStructWithInstance: cResult)
    }

}
