

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
#include "smoke/InternalClassInherits.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InternalClassInherits = ::smoke::InternalClassInherits;

class InternalClassInheritsTrampoline : public InternalClassInherits {
public:
    using InternalClassInherits::InternalClassInherits;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<InternalClassInherits> m_impl;

    void foo_bar(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->foo_bar();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, InternalClassInherits, foo_bar);
    }
    ::std::string get_prop() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_prop();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, InternalClassInherits, get_prop);
    }
    void set_prop(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_prop(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, InternalClassInherits, set_prop, value);
    }
};

void register_smoke_InternalClassInherits(py::module_& module) {
    py::class_<InternalClassInherits, ::smoke::InternalInterfaceParent, std::shared_ptr<InternalClassInherits>, InternalClassInheritsTrampoline>(module, "smoke_InternalClassInherits")
        .def("__gluecodium_id__", [](const InternalClassInherits& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<InternalClassInherits> native) {
            auto self = std::make_shared<InternalClassInheritsTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("foo_bar", [](InternalClassInherits& self) {
            return self.foo_bar();
        })
        .def_property("prop", [](const InternalClassInherits& self) {
            return self.get_prop();
        }, [](InternalClassInherits& self, const ::std::string& value) {
            self.set_prop(value);
        })
        ;
}

