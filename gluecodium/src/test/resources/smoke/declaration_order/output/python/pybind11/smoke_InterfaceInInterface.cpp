

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/InterfaceInInterface.h"
#include "functional"
#include "memory"

using InterfaceInInterface = ::smoke::InterfaceInInterface;
using FooChecker = ::smoke::InterfaceInInterface::FooChecker;

class InterfaceInInterfaceTrampoline : public InterfaceInInterface {
public:
    using InterfaceInInterface::InterfaceInInterface;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<InterfaceInInterface> m_impl;

};

class FooCheckerTrampoline : public FooChecker {
public:
    using FooChecker::FooChecker;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<FooChecker> m_impl;

};



void register_smoke_InterfaceInInterface(py::module_& module) {
auto cls_InterfaceInInterface = py::class_<InterfaceInInterface, std::shared_ptr<InterfaceInInterface>, InterfaceInInterfaceTrampoline>(module, "smoke_InterfaceInInterface")
        .def("__gluecodium_id__", [](const InterfaceInInterface& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<InterfaceInInterface> native) {
            auto self = std::make_shared<InterfaceInInterfaceTrampoline>();
            self->m_impl = native;
            return self;
        }))
        ;

auto cls_InterfaceInInterfaceFooChecker = py::class_<FooChecker, std::shared_ptr<FooChecker>, FooCheckerTrampoline>(cls_InterfaceInInterface, "FooChecker")
        .def("__gluecodium_id__", [](const FooChecker& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<FooChecker> native) {
            auto self = std::make_shared<FooCheckerTrampoline>();
            self->m_impl = native;
            return self;
        }))
        ;


}
