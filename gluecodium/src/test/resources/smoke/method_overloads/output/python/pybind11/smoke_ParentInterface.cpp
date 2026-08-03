

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
#include "smoke/ParentInterface.h"
#include "cstdint"

using ParentInterface = ::smoke::ParentInterface;

class ParentInterfaceTrampoline : public ParentInterface {
public:
    using ParentInterface::ParentInterface;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ParentInterface> m_impl;

    void foo(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->foo();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ParentInterface, foo);
    }
    void foo(
            int32_t input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->foo(input);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ParentInterface, foo, input);
    }
    void bar(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->bar();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ParentInterface, bar);
    }
    void baz(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->baz();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ParentInterface, baz);
    }
};



void register_smoke_ParentInterface(py::module_& module) {
auto cls_ParentInterface = py::class_<ParentInterface, std::shared_ptr<ParentInterface>, ParentInterfaceTrampoline>(module, "smoke_ParentInterface")
        .def("__gluecodium_id__", [](const ParentInterface& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<ParentInterface> native) {
            auto self = std::make_shared<ParentInterfaceTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("foo", [](ParentInterface& self) {
            return self.foo();
        })
        .def("foo", [](ParentInterface& self, const int32_t input) {
            return self.foo(input);
        }, py::arg("input"))
        .def("bar", [](ParentInterface& self) {
            return self.bar();
        })
        .def("baz", [](ParentInterface& self) {
            return self.baz();
        })
        ;


}
