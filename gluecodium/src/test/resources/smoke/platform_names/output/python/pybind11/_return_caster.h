

// Custom pybind11 type_caster for Gluecodium's Return<T, Error> adapter.
//
// On success (has_value): the inner value is returned to Python automatically
// (delegating to pybind11's built-in casters for the value type).
// On failure: a Python exception is raised carrying the error description.
//
// The error string is derived via a small traits helper so the same caster
// works for both std::error_code and user-defined error types.

#pragma once

#include <pybind11/pybind11.h>
#include <cstdint>
#include <memory>
#include <string>
#include <system_error>
#include <type_traits>
#include <vector>

#include "_wrapper_cache.h"
#include <gluecodium/Return.h>

namespace pybind11::detail {

// Gluecodium blobs are represented in C++ as shared vectors and in Python as bytes.
template <>
struct type_caster<std::shared_ptr<std::vector<uint8_t>>> {
    PYBIND11_TYPE_CASTER(std::shared_ptr<std::vector<uint8_t>>, _("bytes"));

    bool load(handle source, bool) {
        if (!pybind11::isinstance<pybind11::bytes>(source)) return false;
        const std::string data = pybind11::cast<std::string>(source);
        value = std::make_shared<std::vector<uint8_t>>(data.begin(), data.end());
        return true;
    }

    static handle cast(const std::shared_ptr<std::vector<uint8_t>>& source,
                       return_value_policy,
                       handle) {
        if (!source) return pybind11::none().release();
        return pybind11::bytes(reinterpret_cast<const char*>(source->data()), source->size()).release();
    }
};

// Traits to stringify an error of arbitrary type.
template <typename Error, typename = void>
struct ReturnErrorToString {
    static std::string convert(const Error&) { return "unknown error"; }
};

template <typename Error>
struct ReturnErrorToString<
    Error, std::void_t<decltype(std::declval<Error>().message())>> {
    static std::string convert(const Error& e) { return e.message(); }
};

template <>
struct ReturnErrorToString<std::error_code> {
    static std::string convert(const std::error_code& e) {
        return e.message().empty() ? "error" : e.message();
    }
};

template <typename Value, typename Error>
struct type_caster<gluecodium::Return<Value, Error>> {
    using ReturnT = gluecodium::Return<Value, Error>;
    PYBIND11_TYPE_CASTER(ReturnT, _("Return[T, Error]"));

    // Convert C++ Return -> Python.
    static handle cast(const gluecodium::Return<Value, Error>& src,
                       return_value_policy policy, handle parent) {
        if (src.has_value()) {
            if constexpr (std::is_void_v<Value>) {
                return pybind11::none().release();
            } else {
                return type_caster<Value>::cast(src.unsafe_value(), policy, parent);
            }
        }
        // Failure: set a Python exception carrying the error description, then
        // throw error_already_set so pybind11 propagates it (instead of wrapping
        // a null handle as a generic TypeError).
        const std::string msg = ReturnErrorToString<Error>::convert(src.error());
        PyErr_SetString(PyExc_RuntimeError, msg.c_str());
        throw pybind11::error_already_set();
    }

    // Python -> C++ is not supported (Return is an output-only adapter).
    bool load(handle, bool) { return false; }
};

}  // namespace pybind11::detail
