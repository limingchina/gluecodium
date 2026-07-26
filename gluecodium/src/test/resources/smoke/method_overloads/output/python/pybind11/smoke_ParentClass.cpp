

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ParentClass.h"
#include "cstdint"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
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
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->foo();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ParentClass, foo);
    }
    void foo(
            int32_t input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->foo(input);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ParentClass, foo, input);
    }
    void bar(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->bar();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ParentClass, bar);
    }
    void baz(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->baz();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ParentClass, baz);
    }
};

void register_smoke_ParentClass(py::module_& module) {
    py::class_<ParentClass, std::shared_ptr<ParentClass>, ParentClassTrampoline>(module, "smoke_ParentClass")
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
        .def("foo", py::overload_cast<>(&ParentClass::foo))
        .def("foo", py::overload_cast<const int32_t>(&ParentClass::foo), py::arg("input"))
        .def("bar", py::overload_cast<>(&ParentClass::bar))
        .def("baz", &ParentClass::baz)
        ;
}

