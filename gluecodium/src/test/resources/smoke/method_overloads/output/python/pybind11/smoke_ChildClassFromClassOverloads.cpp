

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ChildClassFromClassOverloads.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ChildClassFromClassOverloads = ::smoke::ChildClassFromClassOverloads;

class ChildClassFromClassOverloadsTrampoline : public ChildClassFromClassOverloads {
public:
    using ChildClassFromClassOverloads::ChildClassFromClassOverloads;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ChildClassFromClassOverloads> m_impl;

    void foo(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->foo(input);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassFromClassOverloads, foo, input);
    }
    void foo(
            double input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->foo(input);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassFromClassOverloads, foo, input);
    }
    void bar(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->bar(input);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassFromClassOverloads, bar, input);
    }
    void bar(
            double input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->bar(input);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassFromClassOverloads, bar, input);
    }
    void foo(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->foo();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassFromClassOverloads, foo);
    }
    void foo(
            int32_t input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->foo(input);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassFromClassOverloads, foo, input);
    }
    void bar(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->bar();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassFromClassOverloads, bar);
    }
    void baz(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->baz();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassFromClassOverloads, baz);
    }
};

void register_smoke_ChildClassFromClassOverloads(py::module_& module) {
    py::class_<ChildClassFromClassOverloads, ::smoke::ParentClass, std::shared_ptr<ChildClassFromClassOverloads>, ChildClassFromClassOverloadsTrampoline>(module, "ChildClassFromClassOverloads")
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<ChildClassFromClassOverloads> native) {
            auto self = std::make_shared<ChildClassFromClassOverloadsTrampoline>();
            self->m_impl = native;
            return self;
        }))
        ;
}

