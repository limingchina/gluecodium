

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/OuterClassWithInheritance.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using OuterClassWithInheritance = ::smoke::OuterClassWithInheritance;

class OuterClassWithInheritanceTrampoline : public OuterClassWithInheritance {
public:
    using OuterClassWithInheritance::OuterClassWithInheritance;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<OuterClassWithInheritance> m_impl;

    ::std::string foo(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->foo(input);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, OuterClassWithInheritance, foo, input);
    }
    void parent_fun(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->parent_fun();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, OuterClassWithInheritance, parent_fun);
    }
    ::std::string get_parent_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_parent_property();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, OuterClassWithInheritance, get_parent_property);
    }
    void set_parent_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_parent_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, OuterClassWithInheritance, set_parent_property, value);
    }
};

void register_OuterClassWithInheritance(py::module_& module) {
    py::class_<OuterClassWithInheritance, std::shared_ptr<OuterClassWithInheritance>, OuterClassWithInheritanceTrampoline>(module, "OuterClassWithInheritance")
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<OuterClassWithInheritance> native) {
            auto self = std::make_shared<OuterClassWithInheritanceTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("foo", &OuterClassWithInheritance::foo, py::arg("input"))

        ;
}

