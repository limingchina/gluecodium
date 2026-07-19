

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ForwardDeclarationBug.h"
#include "smoke/ParentClass.h"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ForwardDeclarationBug = ::smoke::ForwardDeclarationBug;

class ForwardDeclarationBugTrampoline : public ForwardDeclarationBug {
public:
    using ForwardDeclarationBug::ForwardDeclarationBug;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ForwardDeclarationBug> m_impl;

    void foo(
            const ::std::shared_ptr< ::smoke::ParentClass >& bar ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->foo(bar);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ForwardDeclarationBug, foo, bar);
    }
    void root_method(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->root_method();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ForwardDeclarationBug, root_method);
    }
    ::std::string get_root_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_root_property();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, ForwardDeclarationBug, get_root_property);
    }
    void set_root_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_root_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ForwardDeclarationBug, set_root_property, value);
    }
};

void register_ForwardDeclarationBug(py::module_& module) {
    py::class_<ForwardDeclarationBug, std::shared_ptr<ForwardDeclarationBug>, ForwardDeclarationBugTrampoline>(module, "ForwardDeclarationBug")
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<ForwardDeclarationBug> native) {
            auto self = std::make_shared<ForwardDeclarationBugTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("foo", &ForwardDeclarationBug::foo, py::arg("bar"))

        ;
}

