

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/Optional.h"
#include "smoke/ListenerWithNullable.h"
#include "cstdint"

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

    ::gluecodium::optional< int8_t > method_with_byte(
            const ::gluecodium::optional< int8_t >& input ) override {
        if (m_impl) {
            return m_impl->method_with_byte(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ListenerWithNullable*>(this), "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f645769746842797465")) {
        PYBIND11_OVERRIDE_PURE_NAME(::gluecodium::optional< int8_t >, ListenerWithNullable, "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f645769746842797465", method_with_byte, input);
        }
        PYBIND11_OVERRIDE_PURE(::gluecodium::optional< int8_t >, ListenerWithNullable, method_with_byte, input);
    }
    ::gluecodium::optional< uint8_t > method_with_u_byte(
            const ::gluecodium::optional< uint8_t >& input ) override {
        if (m_impl) {
            return m_impl->method_with_u_byte(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ListenerWithNullable*>(this), "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f64576974685542797465")) {
        PYBIND11_OVERRIDE_PURE_NAME(::gluecodium::optional< uint8_t >, ListenerWithNullable, "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f64576974685542797465", method_with_u_byte, input);
        }
        PYBIND11_OVERRIDE_PURE(::gluecodium::optional< uint8_t >, ListenerWithNullable, method_with_u_byte, input);
    }
    ::gluecodium::optional< int16_t > method_with_short(
            const ::gluecodium::optional< int16_t >& input ) override {
        if (m_impl) {
            return m_impl->method_with_short(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ListenerWithNullable*>(this), "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f645769746853686f7274")) {
        PYBIND11_OVERRIDE_PURE_NAME(::gluecodium::optional< int16_t >, ListenerWithNullable, "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f645769746853686f7274", method_with_short, input);
        }
        PYBIND11_OVERRIDE_PURE(::gluecodium::optional< int16_t >, ListenerWithNullable, method_with_short, input);
    }
    ::gluecodium::optional< uint16_t > method_with_u_short(
            const ::gluecodium::optional< uint16_t >& input ) override {
        if (m_impl) {
            return m_impl->method_with_u_short(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ListenerWithNullable*>(this), "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f64576974685553686f7274")) {
        PYBIND11_OVERRIDE_PURE_NAME(::gluecodium::optional< uint16_t >, ListenerWithNullable, "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f64576974685553686f7274", method_with_u_short, input);
        }
        PYBIND11_OVERRIDE_PURE(::gluecodium::optional< uint16_t >, ListenerWithNullable, method_with_u_short, input);
    }
    ::gluecodium::optional< int32_t > method_with_int(
            const ::gluecodium::optional< int32_t >& input ) override {
        if (m_impl) {
            return m_impl->method_with_int(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ListenerWithNullable*>(this), "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f6457697468496e74")) {
        PYBIND11_OVERRIDE_PURE_NAME(::gluecodium::optional< int32_t >, ListenerWithNullable, "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f6457697468496e74", method_with_int, input);
        }
        PYBIND11_OVERRIDE_PURE(::gluecodium::optional< int32_t >, ListenerWithNullable, method_with_int, input);
    }
    ::gluecodium::optional< uint32_t > method_with_u_int(
            const ::gluecodium::optional< uint32_t >& input ) override {
        if (m_impl) {
            return m_impl->method_with_u_int(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ListenerWithNullable*>(this), "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f645769746855496e74")) {
        PYBIND11_OVERRIDE_PURE_NAME(::gluecodium::optional< uint32_t >, ListenerWithNullable, "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f645769746855496e74", method_with_u_int, input);
        }
        PYBIND11_OVERRIDE_PURE(::gluecodium::optional< uint32_t >, ListenerWithNullable, method_with_u_int, input);
    }
    ::gluecodium::optional< int64_t > method_with_long(
            const ::gluecodium::optional< int64_t >& input ) override {
        if (m_impl) {
            return m_impl->method_with_long(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ListenerWithNullable*>(this), "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f64576974684c6f6e67")) {
        PYBIND11_OVERRIDE_PURE_NAME(::gluecodium::optional< int64_t >, ListenerWithNullable, "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f64576974684c6f6e67", method_with_long, input);
        }
        PYBIND11_OVERRIDE_PURE(::gluecodium::optional< int64_t >, ListenerWithNullable, method_with_long, input);
    }
    ::gluecodium::optional< uint64_t > method_with_u_long(
            const ::gluecodium::optional< uint64_t >& input ) override {
        if (m_impl) {
            return m_impl->method_with_u_long(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ListenerWithNullable*>(this), "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f6457697468554c6f6e67")) {
        PYBIND11_OVERRIDE_PURE_NAME(::gluecodium::optional< uint64_t >, ListenerWithNullable, "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f6457697468554c6f6e67", method_with_u_long, input);
        }
        PYBIND11_OVERRIDE_PURE(::gluecodium::optional< uint64_t >, ListenerWithNullable, method_with_u_long, input);
    }
    ::gluecodium::optional< bool > method_with_double(
            const ::gluecodium::optional< bool >& input ) override {
        if (m_impl) {
            return m_impl->method_with_double(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ListenerWithNullable*>(this), "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f6457697468446f75626c65")) {
        PYBIND11_OVERRIDE_PURE_NAME(::gluecodium::optional< bool >, ListenerWithNullable, "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f6457697468446f75626c65", method_with_double, input);
        }
        PYBIND11_OVERRIDE_PURE(::gluecodium::optional< bool >, ListenerWithNullable, method_with_double, input);
    }
    ::gluecodium::optional< float > method_with_float(
            const ::gluecodium::optional< float >& input ) override {
        if (m_impl) {
            return m_impl->method_with_float(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ListenerWithNullable*>(this), "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f6457697468466c6f6174")) {
        PYBIND11_OVERRIDE_PURE_NAME(::gluecodium::optional< float >, ListenerWithNullable, "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f6457697468466c6f6174", method_with_float, input);
        }
        PYBIND11_OVERRIDE_PURE(::gluecodium::optional< float >, ListenerWithNullable, method_with_float, input);
    }
    ::gluecodium::optional< double > method_with_double(
            const ::gluecodium::optional< double >& input ) override {
        if (m_impl) {
            return m_impl->method_with_double(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ListenerWithNullable*>(this), "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f6457697468446f75626c653a31")) {
        PYBIND11_OVERRIDE_PURE_NAME(::gluecodium::optional< double >, ListenerWithNullable, "__gluecodium_callback_736d6f6b652e4c697374656e6572576974684e756c6c61626c652e6d6574686f6457697468446f75626c653a31", method_with_double, input);
        }
        PYBIND11_OVERRIDE_PURE(::gluecodium::optional< double >, ListenerWithNullable, method_with_double, input);
    }
};



void register_smoke_ListenerWithNullable(py::module_& module) {
auto cls_ListenerWithNullable = py::class_<ListenerWithNullable, std::shared_ptr<ListenerWithNullable>, ListenerWithNullableTrampoline>(module, "smoke_ListenerWithNullable")
        .def("__gluecodium_id__", [](const ListenerWithNullable& self) {
            return gluecodium::python::native_identity(self);
        })
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
        .def("method_with_byte", [](ListenerWithNullable& self, const ::gluecodium::optional< int8_t >& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.method_with_byte(input); });
        }, py::arg("input"))
        .def("method_with_u_byte", [](ListenerWithNullable& self, const ::gluecodium::optional< uint8_t >& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.method_with_u_byte(input); });
        }, py::arg("input"))
        .def("method_with_short", [](ListenerWithNullable& self, const ::gluecodium::optional< int16_t >& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.method_with_short(input); });
        }, py::arg("input"))
        .def("method_with_u_short", [](ListenerWithNullable& self, const ::gluecodium::optional< uint16_t >& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.method_with_u_short(input); });
        }, py::arg("input"))
        .def("method_with_int", [](ListenerWithNullable& self, const ::gluecodium::optional< int32_t >& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.method_with_int(input); });
        }, py::arg("input"))
        .def("method_with_u_int", [](ListenerWithNullable& self, const ::gluecodium::optional< uint32_t >& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.method_with_u_int(input); });
        }, py::arg("input"))
        .def("method_with_long", [](ListenerWithNullable& self, const ::gluecodium::optional< int64_t >& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.method_with_long(input); });
        }, py::arg("input"))
        .def("method_with_u_long", [](ListenerWithNullable& self, const ::gluecodium::optional< uint64_t >& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.method_with_u_long(input); });
        }, py::arg("input"))
        .def("method_with_double", [](ListenerWithNullable& self, const ::gluecodium::optional< bool >& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.method_with_double(input); });
        }, py::arg("input"))
        .def("method_with_float", [](ListenerWithNullable& self, const ::gluecodium::optional< float >& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.method_with_float(input); });
        }, py::arg("input"))
        .def("method_with_double", [](ListenerWithNullable& self, const ::gluecodium::optional< double >& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.method_with_double(input); });
        }, py::arg("input"))
        ;


}
