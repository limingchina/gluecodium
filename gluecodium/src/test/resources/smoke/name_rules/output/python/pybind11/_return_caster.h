

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
#include <string>
#include <system_error>
#include <type_traits>

#include "_wrapper_cache.h"
#include <Return.h>

namespace pybind11::detail {

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
struct type_caster<::Return<Value, Error>> {
    using ReturnT = ::Return<Value, Error>;
    PYBIND11_TYPE_CASTER(ReturnT, _("Return[T, Error]"));

    // Convert C++ Return -> Python.
    static handle cast(const ::Return<Value, Error>& src,
                       return_value_policy policy, handle parent) {
        if (src.has_value()) {
            return type_caster<Value>::cast(src.unsafe_value(), policy, parent);
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
