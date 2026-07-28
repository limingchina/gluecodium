

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
#include "smoke/InternalInterfaceParent.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InternalInterfaceParent = ::smoke::InternalInterfaceParent;

class InternalInterfaceParentTrampoline : public InternalInterfaceParent {
public:
    using InternalInterfaceParent::InternalInterfaceParent;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<InternalInterfaceParent> m_impl;

    void foo_bar(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->foo_bar();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, InternalInterfaceParent, foo_bar);
    }
    ::std::string get_prop() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_prop();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, InternalInterfaceParent, get_prop);
    }
    void set_prop(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_prop(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, InternalInterfaceParent, set_prop, value);
    }
};

void register_smoke_InternalInterfaceParent(py::module_& module) {
    py::class_<InternalInterfaceParent, std::shared_ptr<InternalInterfaceParent>, InternalInterfaceParentTrampoline>(module, "smoke_InternalInterfaceParent")
        .def("__gluecodium_id__", [](const InternalInterfaceParent& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<InternalInterfaceParent> native) {
            auto self = std::make_shared<InternalInterfaceParentTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("foo_bar", [](InternalInterfaceParent& self) {
            return self.foo_bar();
        })
        .def_property("prop", [](const InternalInterfaceParent& self) {
            return self.get_prop();
        }, [](InternalInterfaceParent& self, const ::std::string& value) {
            self.set_prop(value);
        })
        ;
}

