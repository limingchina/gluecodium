

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
#include "smoke/OuterClass.h"
#include "string"

using OuterClass = ::smoke::OuterClass;
using InnerClass = ::smoke::OuterClass::InnerClass;
using InnerInterface = ::smoke::OuterClass::InnerInterface;

class InnerInterfaceTrampoline : public InnerInterface {
public:
    using InnerInterface::InnerInterface;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<InnerInterface> m_impl;

    ::std::string foo(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->foo(input);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, InnerInterface, foo, input);
    }
};



void register_smoke_OuterClass(py::module_& module) {
auto cls_OuterClass = py::class_<OuterClass, std::shared_ptr<OuterClass>>(module, "smoke_OuterClass")
        .def("__gluecodium_id__", [](const OuterClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("foo", &OuterClass::foo, py::arg("input"))
        ;

auto cls_OuterClassInnerClass = py::class_<InnerClass, std::shared_ptr<InnerClass>>(cls_OuterClass, "InnerClass")
        .def("__gluecodium_id__", [](const InnerClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("foo", &InnerClass::foo, py::arg("input"))
        ;

auto cls_OuterClassInnerInterface = py::class_<InnerInterface, std::shared_ptr<InnerInterface>, InnerInterfaceTrampoline>(cls_OuterClass, "InnerInterface")
        .def("__gluecodium_id__", [](const InnerInterface& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<InnerInterface> native) {
            auto self = std::make_shared<InnerInterfaceTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("foo", [](InnerInterface& self, const ::std::string& input) {
            return self.foo(input);
        }, py::arg("input"))
        ;


}
