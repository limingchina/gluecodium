

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
#include "smoke/OuterClassWithInheritance.h"
#include "string"

using OuterClassWithInheritance = ::smoke::OuterClassWithInheritance;
using InnerClass = ::smoke::OuterClassWithInheritance::InnerClass;
using InnerInterface = ::smoke::OuterClassWithInheritance::InnerInterface;

class OuterClassWithInheritanceTrampoline : public OuterClassWithInheritance {
public:
    using OuterClassWithInheritance::OuterClassWithInheritance;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<OuterClassWithInheritance> m_impl;

    ::std::string foo(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->foo(input);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, OuterClassWithInheritance, foo, input);
    }
    void parent_fun(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->parent_fun();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, OuterClassWithInheritance, parent_fun);
    }
    ::std::string get_parent_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_parent_property();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, OuterClassWithInheritance, get_parent_property);
    }
    void set_parent_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_parent_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, OuterClassWithInheritance, set_parent_property, value);
    }
};

class InnerInterfaceTrampoline : public InnerInterface {
public:
    using InnerInterface::InnerInterface;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<InnerInterface> m_impl;

    ::std::string baz(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->baz(input);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, InnerInterface, baz, input);
    }
};



void register_smoke_OuterClassWithInheritance(py::module_& module) {
auto cls_OuterClassWithInheritance = py::class_<OuterClassWithInheritance, ::smoke::ParentClass, std::shared_ptr<OuterClassWithInheritance>, OuterClassWithInheritanceTrampoline>(module, "smoke_OuterClassWithInheritance")
        .def("__gluecodium_id__", [](const OuterClassWithInheritance& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<OuterClassWithInheritance> native) {
            auto self = std::make_shared<OuterClassWithInheritanceTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("foo", &OuterClassWithInheritance::foo, py::arg("input"))
        .def("parent_fun", &OuterClassWithInheritance::parent_fun)
        .def_property("parent_property", py::overload_cast<>(&OuterClassWithInheritance::get_parent_property, py::const_), py::overload_cast<const ::std::string&>(&OuterClassWithInheritance::set_parent_property))
        ;

auto cls_OuterClassWithInheritanceInnerClass = py::class_<InnerClass, std::shared_ptr<InnerClass>>(cls_OuterClassWithInheritance, "InnerClass")
        .def("__gluecodium_id__", [](const InnerClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("bar", &InnerClass::bar, py::arg("input"))
        ;

auto cls_OuterClassWithInheritanceInnerInterface = py::class_<InnerInterface, std::shared_ptr<InnerInterface>, InnerInterfaceTrampoline>(cls_OuterClassWithInheritance, "InnerInterface")
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
        .def("baz", [](InnerInterface& self, const ::std::string& input) {
            return self.baz(input);
        }, py::arg("input"))
        ;


}
