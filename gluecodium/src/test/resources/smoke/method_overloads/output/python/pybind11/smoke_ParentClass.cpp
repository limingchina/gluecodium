

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
#include "smoke/ParentClass.h"
#include "cstdint"

using ParentClass = ::smoke::ParentClass;

class ParentClassTrampoline : public ParentClass {
public:
    using ParentClass::ParentClass;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ParentClass> m_impl;

    void foo(
            /* no args */ ) override {
        if (m_impl) {
            m_impl->foo();
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ParentClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e666f6f")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, ParentClass, "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e666f6f", foo);
        }
        PYBIND11_OVERRIDE_PURE(void, ParentClass, foo);
    }
    void foo(
            const int32_t input ) override {
        if (m_impl) {
            m_impl->foo(input);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ParentClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e666f6f3a31")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, ParentClass, "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e666f6f3a31", foo, input);
        }
        PYBIND11_OVERRIDE_PURE(void, ParentClass, foo, input);
    }
    void bar(
            /* no args */ ) override {
        if (m_impl) {
            m_impl->bar();
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ParentClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e626172")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, ParentClass, "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e626172", bar);
        }
        PYBIND11_OVERRIDE_PURE(void, ParentClass, bar);
    }
    void baz(
            /* no args */ ) override {
        if (m_impl) {
            m_impl->baz();
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ParentClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e62617a")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, ParentClass, "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e62617a", baz);
        }
        PYBIND11_OVERRIDE_PURE(void, ParentClass, baz);
    }
};



void register_smoke_ParentClass(py::module_& module) {
auto cls_ParentClass = py::class_<ParentClass, std::shared_ptr<ParentClass>, ParentClassTrampoline>(module, "smoke_ParentClass")
        .def("__gluecodium_id__", [](const ParentClass& self) {
            return gluecodium::python::native_identity(self);
        })
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<ParentClass> native) {
            auto self = std::make_shared<ParentClassTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("foo", py::overload_cast<>(&ParentClass::foo), py::call_guard<py::gil_scoped_release>())
        .def("foo", py::overload_cast<const int32_t>(&ParentClass::foo), py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def("bar", py::overload_cast<>(&ParentClass::bar), py::call_guard<py::gil_scoped_release>())
        .def("baz", &ParentClass::baz, py::call_guard<py::gil_scoped_release>())
        ;


}
