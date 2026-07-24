

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ListenerWithNullable.h"
#include "cstdint"
#include "optional"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ListenerWithNullable = ::smoke::ListenerWithNullable;

class ListenerWithNullableTrampoline : public ListenerWithNullable {
public:
    using ListenerWithNullable::ListenerWithNullable;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ListenerWithNullable> m_impl;

    std::optional< int8_t > method_with_byte(
            const std::optional< int8_t >& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->method_with_byte(input);
        }
        PYBIND11_OVERRIDE_PURE(std::optional< int8_t >, ListenerWithNullable, method_with_byte, input);
    }
    std::optional< uint8_t > method_with_u_byte(
            const std::optional< uint8_t >& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->method_with_u_byte(input);
        }
        PYBIND11_OVERRIDE_PURE(std::optional< uint8_t >, ListenerWithNullable, method_with_u_byte, input);
    }
    std::optional< int16_t > method_with_short(
            const std::optional< int16_t >& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->method_with_short(input);
        }
        PYBIND11_OVERRIDE_PURE(std::optional< int16_t >, ListenerWithNullable, method_with_short, input);
    }
    std::optional< uint16_t > method_with_u_short(
            const std::optional< uint16_t >& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->method_with_u_short(input);
        }
        PYBIND11_OVERRIDE_PURE(std::optional< uint16_t >, ListenerWithNullable, method_with_u_short, input);
    }
    std::optional< int32_t > method_with_int(
            const std::optional< int32_t >& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->method_with_int(input);
        }
        PYBIND11_OVERRIDE_PURE(std::optional< int32_t >, ListenerWithNullable, method_with_int, input);
    }
    std::optional< uint32_t > method_with_u_int(
            const std::optional< uint32_t >& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->method_with_u_int(input);
        }
        PYBIND11_OVERRIDE_PURE(std::optional< uint32_t >, ListenerWithNullable, method_with_u_int, input);
    }
    std::optional< int64_t > method_with_long(
            const std::optional< int64_t >& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->method_with_long(input);
        }
        PYBIND11_OVERRIDE_PURE(std::optional< int64_t >, ListenerWithNullable, method_with_long, input);
    }
    std::optional< uint64_t > method_with_u_long(
            const std::optional< uint64_t >& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->method_with_u_long(input);
        }
        PYBIND11_OVERRIDE_PURE(std::optional< uint64_t >, ListenerWithNullable, method_with_u_long, input);
    }
    std::optional< bool > method_with_double(
            const std::optional< bool >& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->method_with_double(input);
        }
        PYBIND11_OVERRIDE_PURE(std::optional< bool >, ListenerWithNullable, method_with_double, input);
    }
    std::optional< float > method_with_float(
            const std::optional< float >& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->method_with_float(input);
        }
        PYBIND11_OVERRIDE_PURE(std::optional< float >, ListenerWithNullable, method_with_float, input);
    }
    std::optional< double > method_with_double(
            const std::optional< double >& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->method_with_double(input);
        }
        PYBIND11_OVERRIDE_PURE(std::optional< double >, ListenerWithNullable, method_with_double, input);
    }
};

void register_smoke_ListenerWithNullable(py::module_& module) {
    py::class_<ListenerWithNullable, std::shared_ptr<ListenerWithNullable>, ListenerWithNullableTrampoline>(module, "ListenerWithNullable")
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<ListenerWithNullable> native) {
            auto self = std::make_shared<ListenerWithNullableTrampoline>();
            self->m_impl = native;
            return self;
        }))
        ;
}

