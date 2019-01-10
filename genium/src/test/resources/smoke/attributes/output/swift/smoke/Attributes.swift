//
//
// Automatically generated. Do not modify. Your changes will be lost.

import Foundation

internal func getRef(_ ref: Attributes?, owning: Bool = true) -> RefHolder {
    guard let c_handle = ref?.c_instance else {
        return RefHolder(0)
    }
    let handle_copy = smoke_Attributes_copy_handle(c_handle)
    return owning
        ? RefHolder(ref: handle_copy, release: smoke_Attributes_release_handle)
        : RefHolder(handle_copy)
}
public class Attributes {

    public var builtInTypeAttribute: UInt32 {
        get {
            return smoke_Attributes_builtInTypeAttribute_get(c_instance)
        }
        set {
            return smoke_Attributes_builtInTypeAttribute_set(c_instance, newValue)
        }
    }

    public var readonlyAttribute: Float {
        get {
            return smoke_Attributes_readonlyAttribute_get(c_instance)
        }

    }

    public var structAttribute: Attributes.ExampleStruct {
        get {
            let cResult = smoke_Attributes_structAttribute_get(c_instance)
            defer {
                smoke_Attributes_ExampleStruct_release_handle(cResult)
            }
            return Attributes.ExampleStruct(cExampleStruct: cResult)
        }
        set {
            let newValue_handle = newValue.convertToCType()
            defer {
                smoke_Attributes_ExampleStruct_release_handle(newValue_handle)
            }
            return smoke_Attributes_structAttribute_set(c_instance, newValue_handle)
        }
    }

    public var arrayAttribute: CollectionOf<String> {
        get {

            let result_handle = smoke_Attributes_arrayAttribute_get(c_instance)
            return StringList(result_handle)
        }
        set {

            let newValue_handle = newValue.c_conversion()
            defer {
                newValue_handle.cleanup()
            }
            return smoke_Attributes_arrayAttribute_set(c_instance, newValue_handle.c_type)
        }
    }

    public var complexTypeAttribute: Attributes.InternalError {
        get {
            let cResult = smoke_Attributes_complexTypeAttribute_get(c_instance)
            return Attributes.InternalError(rawValue: cResult)!
        }
        set {
            return smoke_Attributes_complexTypeAttribute_set(c_instance, newValue.rawValue)
        }
    }

    public var byteBufferAttribute: Data {
        get {
            let result_data_handle = smoke_Attributes_byteBufferAttribute_get(c_instance)
            defer {
                byteArray_release_handle(result_data_handle)
            }
            return Data(bytes: byteArray_data_get(result_data_handle), count: Int(byteArray_size_get(result_data_handle)))
        }
        set {
            let newValue_handle = byteArray_create_handle()
            defer {
                byteArray_release_handle(newValue_handle)
            }
            newValue.withUnsafeBytes { (newValue_ptr: UnsafePointer<UInt8>) in
                byteArray_assign(newValue_handle, newValue_ptr, newValue.count)
            }
            return smoke_Attributes_byteBufferAttribute_set(c_instance, newValue_handle)
        }
    }

    public var instanceAttribute: AttributesInterface? {
        get {
            let cResult = smoke_Attributes_instanceAttribute_get(c_instance)
            if cResult == 0 { return nil }
            if let swift_pointer = smoke_AttributesInterface_get_swift_object_from_cache(cResult),
                    let re_constructed = Unmanaged<AnyObject>.fromOpaque(swift_pointer).takeUnretainedValue() as? AttributesInterface {
                return re_constructed
            }
            return _AttributesInterface(cAttributesInterface: cResult)
        }
        set {
            let newValue_handle = getRef(newValue)
            return smoke_Attributes_instanceAttribute_set(c_instance, newValue_handle.ref)
        }
    }

    public var isBooleanAttribute: Bool {
        get {
            return smoke_Attributes_booleanAttribute_get(c_instance)
        }
        set {
            return smoke_Attributes_booleanAttribute_set(c_instance, newValue)
        }
    }

    public static var staticAttribute: String {
        get {
            let result_string_handle = smoke_Attributes_staticAttribute_get()
            defer {
                std_string_release_handle(result_string_handle)
            }
            return String(data: Data(bytes: std_string_data_get(result_string_handle),
                                     count: Int(std_string_size_get(result_string_handle))), encoding: .utf8)!
        }
        set {
            return smoke_Attributes_staticAttribute_set(newValue)
        }
    }

    public static var staticReadonlyAttribute: Attributes.ExampleStruct {
        get {
            let cResult = smoke_Attributes_staticReadonlyAttribute_get()
            defer {
                smoke_Attributes_ExampleStruct_release_handle(cResult)
            }
            return Attributes.ExampleStruct(cExampleStruct: cResult)
        }
    }

    let c_instance : _baseRef

    init(cAttributes: _baseRef) {
        guard cAttributes != 0 else {
            fatalError("Nullptr value is not supported for initializers")
        }
        c_instance = cAttributes
    }

    deinit {
        smoke_Attributes_release_handle(c_instance)
    }
    public enum InternalError : UInt32 {

        case errorNone

        case errorFatal = 999
    }

    public struct ExampleStruct {
        public var value: Double

        public init(value: Double) {
            self.value = value
        }

        internal init(cExampleStruct: _baseRef) {
            value = smoke_Attributes_ExampleStruct_value_get(cExampleStruct)
        }

        internal func convertToCType() -> _baseRef {
            let value_handle = value
            return smoke_Attributes_ExampleStruct_create_handle(value_handle)
        }
    }

}

extension Attributes: NativeBase {
    var c_handle: _baseRef { return c_instance }
}
