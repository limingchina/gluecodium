

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
#include "smoke/GrandChildInterface.h"

using GrandChildInterface = ::smoke::GrandChildInterface;

class GrandChildInterfaceTrampoline : public GrandChildInterface {
public:
    using GrandChildInterface::GrandChildInterface;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<GrandChildInterface> m_impl;

    void grand_child_method(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->grand_child_method();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, GrandChildInterface, grand_child_method);
    }
    void child_method(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->child_method();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, GrandChildInterface, child_method);
    }
    void root_method(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->root_method();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, GrandChildInterface, root_method);
    }
    ::std::string get_root_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_root_property();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, GrandChildInterface, get_root_property);
    }
    void set_root_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_root_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, GrandChildInterface, set_root_property, value);
    }
};



void register_smoke_GrandChildInterface(py::module_& module) {
auto cls_GrandChildInterface = py::class_<GrandChildInterface, ::smoke::ChildInterface, std::shared_ptr<GrandChildInterface>, GrandChildInterfaceTrampoline>(module, "smoke_GrandChildInterface")
        .def("__gluecodium_id__", [](const GrandChildInterface& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<GrandChildInterface> native) {
            auto self = std::make_shared<GrandChildInterfaceTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("grand_child_method", [](GrandChildInterface& self) {
            return self.grand_child_method();
        })
        .def("child_method", [](GrandChildInterface& self) {
            return self.child_method();
        })
        .def("root_method", [](GrandChildInterface& self) {
            return self.root_method();
        })
        .def_property("root_property", [](const GrandChildInterface& self) {
            return self.get_root_property();
        }, [](GrandChildInterface& self, const ::std::string& value) {
            self.set_root_property(value);
        })
        ;


}
