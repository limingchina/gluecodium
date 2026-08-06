

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
#include "smoke/ChildInterface.h"
#include "smoke/ParentInterface.h"
#include "string"

using ChildInterface = ::smoke::ChildInterface;

class ChildInterfaceTrampoline : public ChildInterface {
public:
    using ChildInterface::ChildInterface;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ChildInterface> m_impl;

    void child_method(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->child_method();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ChildInterface, child_method);
    }
    void root_method(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->root_method();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ChildInterface, root_method);
    }
    ::std::string get_root_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_root_property();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, ChildInterface, get_root_property);
    }
    void set_root_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_root_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ChildInterface, set_root_property, value);
    }
};



void register_smoke_ChildInterface(py::module_& module) {
auto cls_ChildInterface = py::class_<ChildInterface, ::smoke::ParentInterface, std::shared_ptr<ChildInterface>, ChildInterfaceTrampoline>(module, "smoke_ChildInterface")
        .def("__gluecodium_id__", [](const ChildInterface& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<ChildInterface> native) {
            auto self = std::make_shared<ChildInterfaceTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("child_method", [](ChildInterface& self) {
            return self.child_method();
        })
        .def("root_method", [](ChildInterface& self) {
            return self.root_method();
        })
        .def_property("root_property", [](const ChildInterface& self) {
            return self.get_root_property();
        }, [](ChildInterface& self, const ::std::string& value) {
            self.set_root_property(value);
        })
        ;


}
