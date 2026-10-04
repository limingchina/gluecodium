

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
#include "smoke/OuterClassWithInheritance.h"
#include "smoke/ParentClass.h"
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
        if (py::get_override(static_cast<const OuterClassWithInheritance*>(this), "__gluecodium_callback_736d6f6b652e4f75746572436c61737357697468496e6865726974616e63652e666f6f")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, OuterClassWithInheritance, "__gluecodium_callback_736d6f6b652e4f75746572436c61737357697468496e6865726974616e63652e666f6f", foo, input);
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
        if (py::get_override(static_cast<const OuterClassWithInheritance*>(this), "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7446756e")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, OuterClassWithInheritance, "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7446756e", parent_fun);
        }
        PYBIND11_OVERRIDE_PURE(void, OuterClassWithInheritance, parent_fun);
    }
    ::std::string get_parent_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_parent_property();
        }
        if (py::get_override(static_cast<const OuterClassWithInheritance*>(this), "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7450726f7065727479_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, OuterClassWithInheritance, "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7450726f7065727479_get", get_parent_property);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, OuterClassWithInheritance, get_parent_property);
    }
    void set_parent_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_parent_property(value);
            return;
        }
        if (py::get_override(static_cast<const OuterClassWithInheritance*>(this), "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7450726f7065727479_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, OuterClassWithInheritance, "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7450726f7065727479_set", set_parent_property, value);
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
        if (py::get_override(static_cast<const InnerInterface*>(this), "__gluecodium_callback_736d6f6b652e4f75746572436c61737357697468496e6865726974616e63652e496e6e6572496e746572666163652e62617a")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, InnerInterface, "__gluecodium_callback_736d6f6b652e4f75746572436c61737357697468496e6865726974616e63652e496e6e6572496e746572666163652e62617a", baz, input);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, InnerInterface, baz, input);
    }
};



void register_smoke_OuterClassWithInheritance(py::module_& module) {
auto cls_OuterClassWithInheritance = py::class_<OuterClassWithInheritance, ::smoke::ParentClass, std::shared_ptr<OuterClassWithInheritance>, OuterClassWithInheritanceTrampoline>(module, "smoke_OuterClassWithInheritance")
        .def("__gluecodium_id__", [](const OuterClassWithInheritance& self) {
            return gluecodium::python::native_identity(self);
        })
        .def_static("__gluecodium_downcast__", [](const py::object& native) -> py::object {
            try {
                auto base = native.cast<std::shared_ptr<::smoke::ParentClass>>();
                auto derived = gluecodium::python::dynamic_pointer_cast<OuterClassWithInheritance>(base);
                if (derived) return py::cast(derived);
            } catch (const py::cast_error&) {
            }
            return py::none();
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
            return gluecodium::python::native_identity(self);
        })
        .def("bar", &InnerClass::bar, py::arg("input"))
        ;

auto cls_OuterClassWithInheritanceInnerInterface = py::class_<InnerInterface, std::shared_ptr<InnerInterface>, InnerInterfaceTrampoline>(cls_OuterClassWithInheritance, "InnerInterface")
        .def("__gluecodium_id__", [](const InnerInterface& self) {
            return gluecodium::python::native_identity(self);
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
