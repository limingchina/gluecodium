

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
#include "smoke/forward/InnerClassForwardDeclarations.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InnerClass1 = ::smoke::forward::InnerClassForwardDeclarations::InnerClass1;

class InnerClassForwardDeclarationsInnerClass1Trampoline : public InnerClass1 {
public:
    using InnerClass1::InnerClass1;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<InnerClass1> m_impl;

    ::std::shared_ptr< ::smoke::forward::InnerClassForwardDeclarations::InnerInterface1 > get_inner_interface(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_inner_interface();
        }
        PYBIND11_OVERRIDE_PURE(::std::shared_ptr< ::smoke::forward::InnerClassForwardDeclarations::InnerInterface1 >, InnerClass1, get_inner_interface);
    }
};

void register_smoke_forward_InnerClassForwardDeclarationsInnerClass1(py::module_& module) {
    py::class_<InnerClass1, std::shared_ptr<InnerClass1>, InnerClassForwardDeclarationsInnerClass1Trampoline>(module, "smoke_forward_InnerClassForwardDeclarationsInnerClass1")
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<InnerClass1> native) {
            auto self = std::make_shared<InnerClassForwardDeclarationsInnerClass1Trampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("get_inner_interface", &InnerClass1::get_inner_interface)
        ;
}

