

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
#include "smoke/ChildClassFromInterface.h"
#include "smoke/ParentInterface.h"
#include "string"

using ChildClassFromInterface = ::smoke::ChildClassFromInterface;

class ChildClassFromInterfaceTrampoline : public ChildClassFromInterface {
public:
    using ChildClassFromInterface::ChildClassFromInterface;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ChildClassFromInterface> m_impl;

    void child_class_method(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->child_class_method();
            return;
        }
        if (py::get_override(static_cast<const ChildClassFromInterface*>(this), "__gluecodium_callback_736d6f6b652e4368696c64436c61737346726f6d496e746572666163652e6368696c64436c6173734d6574686f64")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, ChildClassFromInterface, "__gluecodium_callback_736d6f6b652e4368696c64436c61737346726f6d496e746572666163652e6368696c64436c6173734d6574686f64", child_class_method);
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassFromInterface, child_class_method);
    }
    void root_method(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->root_method();
            return;
        }
        if (py::get_override(static_cast<const ChildClassFromInterface*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f744d6574686f64")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, ChildClassFromInterface, "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f744d6574686f64", root_method);
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassFromInterface, root_method);
    }
    ::std::string get_root_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_root_property();
        }
        if (py::get_override(static_cast<const ChildClassFromInterface*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f7450726f7065727479_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, ChildClassFromInterface, "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f7450726f7065727479_get", get_root_property);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, ChildClassFromInterface, get_root_property);
    }
    void set_root_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_root_property(value);
            return;
        }
        if (py::get_override(static_cast<const ChildClassFromInterface*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f7450726f7065727479_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, ChildClassFromInterface, "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f7450726f7065727479_set", set_root_property, value);
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassFromInterface, set_root_property, value);
    }
};



void register_smoke_ChildClassFromInterface(py::module_& module) {
auto cls_ChildClassFromInterface = py::class_<ChildClassFromInterface, ::smoke::ParentInterface, std::shared_ptr<ChildClassFromInterface>, ChildClassFromInterfaceTrampoline>(module, "smoke_ChildClassFromInterface")
        .def("__gluecodium_id__", [](const ChildClassFromInterface& self) {
            return gluecodium::python::native_identity(self);
        })
        .def_static("__gluecodium_downcast__", [](const py::object& native) -> py::object {
            try {
                auto base = native.cast<std::shared_ptr<::smoke::ParentInterface>>();
                auto derived = gluecodium::python::dynamic_pointer_cast<ChildClassFromInterface>(base);
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
        .def(py::init([](std::shared_ptr<ChildClassFromInterface> native) {
            auto self = std::make_shared<ChildClassFromInterfaceTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("child_class_method", &ChildClassFromInterface::child_class_method)
        .def("root_method", [](ChildClassFromInterface& self) {
            return self.root_method();
        })
        .def_property("root_property", [](const ChildClassFromInterface& self) {
            return self.get_root_property();
        }, [](ChildClassFromInterface& self, const ::std::string& value) {
            self.set_root_property(value);
        })
        ;


}
