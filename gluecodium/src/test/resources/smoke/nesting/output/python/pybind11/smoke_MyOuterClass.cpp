

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
#include "smoke/MyOuterClass.h"

using MyOuterClass = ::smoke::MyOuterClass;
using MyNestedImplementation = ::smoke::MyOuterClass::MyNestedImplementation;

class MyNestedImplementationTrampoline : public MyNestedImplementation {
public:
    using MyNestedImplementation::MyNestedImplementation;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<MyNestedImplementation> m_impl;

};



void register_smoke_MyOuterClass(py::module_& module) {
auto cls_MyOuterClass = py::class_<MyOuterClass, std::shared_ptr<MyOuterClass>>(module, "smoke_MyOuterClass")
        .def("__gluecodium_id__", [](const MyOuterClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;

auto cls_MyOuterClassMyNestedImplementation = py::class_<MyNestedImplementation, ::smoke::MyParentInterface, std::shared_ptr<MyNestedImplementation>, MyNestedImplementationTrampoline>(cls_MyOuterClass, "MyNestedImplementation")
        .def("__gluecodium_id__", [](const MyNestedImplementation& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<MyNestedImplementation> native) {
            auto self = std::make_shared<MyNestedImplementationTrampoline>();
            self->m_impl = native;
            return self;
        }))
        ;


}
