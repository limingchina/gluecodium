

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/forward/InnerClassForwardDeclarations.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InnerInterface2 = ::smoke::forward::InnerClassForwardDeclarations::InnerInterface2;

class InnerClassForwardDeclarationsInnerInterface2Trampoline : public InnerInterface2 {
public:
    using InnerInterface2::InnerInterface2;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<InnerInterface2> m_impl;

};

void register_smoke_forward_InnerClassForwardDeclarationsInnerInterface2(py::module_& module) {
    py::class_<InnerInterface2, std::shared_ptr<InnerInterface2>, InnerClassForwardDeclarationsInnerInterface2Trampoline>(module, "InnerClassForwardDeclarationsInnerInterface2")
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<InnerInterface2> native) {
            auto self = std::make_shared<InnerClassForwardDeclarationsInnerInterface2Trampoline>();
            self->m_impl = native;
            return self;
        }))
        ;
}

