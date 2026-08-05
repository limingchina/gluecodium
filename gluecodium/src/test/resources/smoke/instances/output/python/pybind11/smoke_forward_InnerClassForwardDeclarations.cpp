

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
#include "smoke/forward/InnerClassForwardDeclarations.h"
#include "memory"

using InnerClassForwardDeclarations = ::smoke::forward::InnerClassForwardDeclarations;
using InnerClass1 = ::smoke::forward::InnerClassForwardDeclarations::InnerClass1;
using InnerClass2 = ::smoke::forward::InnerClassForwardDeclarations::InnerClass2;
using InnerInnerClass1 = ::smoke::forward::InnerClassForwardDeclarations::InnerClass2::InnerInnerClass1;
using InnerInnerClass2 = ::smoke::forward::InnerClassForwardDeclarations::InnerClass2::InnerInnerClass2;
using InnerInterface1 = ::smoke::forward::InnerClassForwardDeclarations::InnerInterface1;
using InnerInterface2 = ::smoke::forward::InnerClassForwardDeclarations::InnerInterface2;
using InnerInterface3 = ::smoke::forward::InnerClassForwardDeclarations::InnerInterface3;

class InnerClass1Trampoline : public InnerClass1 {
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

class _InnerInterface1Trampoline : public InnerInterface1 {
public:
    using InnerInterface1::InnerInterface1;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<InnerInterface1> m_impl;

};

class InnerInterface2Trampoline : public InnerInterface2 {
public:
    using InnerInterface2::InnerInterface2;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<InnerInterface2> m_impl;

};

class InnerInterface3Trampoline : public InnerInterface3 {
public:
    using InnerInterface3::InnerInterface3;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<InnerInterface3> m_impl;

};



void register_smoke_forward_InnerClassForwardDeclarations(py::module_& module) {
auto cls_InnerClassForwardDeclarations = py::class_<InnerClassForwardDeclarations, std::shared_ptr<InnerClassForwardDeclarations>>(module, "smoke_forward_InnerClassForwardDeclarations")
        .def("__gluecodium_id__", [](const InnerClassForwardDeclarations& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;

auto cls_InnerClassForwardDeclarationsInnerClass1 = py::class_<InnerClass1, std::shared_ptr<InnerClass1>, InnerClass1Trampoline>(cls_InnerClassForwardDeclarations, "InnerClass1")
        .def("__gluecodium_id__", [](const InnerClass1& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<InnerClass1> native) {
            auto self = std::make_shared<InnerClass1Trampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("_get_inner_interface", &InnerClass1::get_inner_interface)
        ;

auto cls_InnerClassForwardDeclarationsInnerClass2 = py::class_<InnerClass2, std::shared_ptr<InnerClass2>>(cls_InnerClassForwardDeclarations, "InnerClass2")
        .def("__gluecodium_id__", [](const InnerClass2& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;

auto cls_InnerClassForwardDeclarationsInnerClass2InnerInnerClass1 = py::class_<InnerInnerClass1, std::shared_ptr<InnerInnerClass1>>(cls_InnerClassForwardDeclarationsInnerClass2, "InnerInnerClass1")
        .def("__gluecodium_id__", [](const InnerInnerClass1& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("foo", &InnerInnerClass1::foo)
        ;

auto cls_InnerClassForwardDeclarationsInnerClass2InnerInnerClass2 = py::class_<InnerInnerClass2, std::shared_ptr<InnerInnerClass2>>(cls_InnerClassForwardDeclarationsInnerClass2, "InnerInnerClass2")
        .def("__gluecodium_id__", [](const InnerInnerClass2& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("bar", &InnerInnerClass2::bar, py::arg("arg"))
        ;

auto cls__InnerClassForwardDeclarationsInnerInterface1 = py::class_<InnerInterface1, std::shared_ptr<InnerInterface1>, _InnerInterface1Trampoline>(cls_InnerClassForwardDeclarations, "_InnerInterface1")
        .def("__gluecodium_id__", [](const InnerInterface1& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<InnerInterface1> native) {
            auto self = std::make_shared<_InnerInterface1Trampoline>();
            self->m_impl = native;
            return self;
        }))
        ;

auto cls_InnerClassForwardDeclarationsInnerInterface2 = py::class_<InnerInterface2, std::shared_ptr<InnerInterface2>, InnerInterface2Trampoline>(cls_InnerClassForwardDeclarations, "InnerInterface2")
        .def("__gluecodium_id__", [](const InnerInterface2& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<InnerInterface2> native) {
            auto self = std::make_shared<InnerInterface2Trampoline>();
            self->m_impl = native;
            return self;
        }))
        ;

auto cls_InnerClassForwardDeclarationsInnerInterface3 = py::class_<InnerInterface3, std::shared_ptr<InnerInterface3>, InnerInterface3Trampoline>(cls_InnerClassForwardDeclarations, "InnerInterface3")
        .def("__gluecodium_id__", [](const InnerInterface3& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<InnerInterface3> native) {
            auto self = std::make_shared<InnerInterface3Trampoline>();
            self->m_impl = native;
            return self;
        }))
        ;


}
