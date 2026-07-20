

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/MyOuterClass.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using MyNestedImplementation = ::smoke::MyOuterClass::MyNestedImplementation;

class MyOuterClassMyNestedImplementationTrampoline : public MyNestedImplementation {
public:
    using MyNestedImplementation::MyNestedImplementation;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<MyNestedImplementation> m_impl;

};

void register_MyOuterClassMyNestedImplementation(py::module_& module) {
    py::class_<MyNestedImplementation, ::smoke::MyParentInterface, std::shared_ptr<MyNestedImplementation>, MyOuterClassMyNestedImplementationTrampoline>(module, "MyOuterClassMyNestedImplementation")
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<MyNestedImplementation> native) {
            auto self = std::make_shared<MyOuterClassMyNestedImplementationTrampoline>();
            self->m_impl = native;
            return self;
        }))
        ;
}

