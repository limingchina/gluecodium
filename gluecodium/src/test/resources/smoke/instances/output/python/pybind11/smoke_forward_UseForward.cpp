

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
#include "smoke/SimpleClass.h"
#include "smoke/SimpleInterface.h"
#include "smoke/forward/Class1.h"
#include "smoke/forward/Class2.h"
#include "smoke/forward/UseForward.h"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using UseForward = ::smoke::forward::UseForward;

class UseForwardTrampoline : public UseForward {
public:
    using UseForward::UseForward;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<UseForward> m_impl;

    void use_it(
            const ::std::shared_ptr< ::smoke::forward::Class1 >& param1, const ::std::shared_ptr< ::smoke::forward::Class2 >& param2, const ::std::shared_ptr< ::smoke::SimpleClass >& simple_class, const ::std::shared_ptr< ::smoke::SimpleInterface >& simple_interface ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->use_it(param1, param2, simple_class, simple_interface);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, UseForward, use_it, param1, param2, simple_class, simple_interface);
    }
};

void register_smoke_forward_UseForward(py::module_& module) {
    py::class_<UseForward, std::shared_ptr<UseForward>, UseForwardTrampoline>(module, "smoke_forward_UseForward")
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<UseForward> native) {
            auto self = std::make_shared<UseForwardTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("use_it", [](UseForward& self, const ::std::shared_ptr< ::smoke::forward::Class1 >& param1, const ::std::shared_ptr< ::smoke::forward::Class2 >& param2, const ::std::shared_ptr< ::smoke::SimpleClass >& simple_class, const ::std::shared_ptr< ::smoke::SimpleInterface >& simple_interface) {
            return self.use_it(param1, param2, simple_class, simple_interface);
        }, py::arg("param1"), py::arg("param2"), py::arg("simple_class"), py::arg("simple_interface"))
        ;
}

