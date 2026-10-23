

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
#include "smoke/ChildClassFromClass.h"
#include "smoke/ParentClass.h"
#include "string"

using ChildClassFromClass = ::smoke::ChildClassFromClass;

class ChildClassFromClassTrampoline : public ChildClassFromClass {
public:
    using ChildClassFromClass::ChildClassFromClass;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ChildClassFromClass> m_impl;

    void child_class_method(
            /* no args */ ) override {
        if (m_impl) {
            m_impl->child_class_method();
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ChildClassFromClass*>(this), "__gluecodium_callback_736d6f6b652e4368696c64436c61737346726f6d436c6173732e6368696c64436c6173734d6574686f64")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, ChildClassFromClass, "__gluecodium_callback_736d6f6b652e4368696c64436c61737346726f6d436c6173732e6368696c64436c6173734d6574686f64", child_class_method);
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassFromClass, child_class_method);
    }
    void root_method(
            /* no args */ ) override {
        if (m_impl) {
            m_impl->root_method();
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ChildClassFromClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e726f6f744d6574686f64")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, ChildClassFromClass, "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e726f6f744d6574686f64", root_method);
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassFromClass, root_method);
    }
    ::std::string get_root_property() const override {
        if (m_impl) {
            return m_impl->get_root_property();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ChildClassFromClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e726f6f7450726f7065727479_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, ChildClassFromClass, "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e726f6f7450726f7065727479_get", get_root_property);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, ChildClassFromClass, get_root_property);
    }
    void set_root_property(const ::std::string& value) override {
        if (m_impl) {
            m_impl->set_root_property(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ChildClassFromClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e726f6f7450726f7065727479_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, ChildClassFromClass, "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e726f6f7450726f7065727479_set", set_root_property, value);
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassFromClass, set_root_property, value);
    }
};



void register_smoke_ChildClassFromClass(py::module_& module) {
auto cls_ChildClassFromClass = py::class_<ChildClassFromClass, ::smoke::ParentClass, std::shared_ptr<ChildClassFromClass>, ChildClassFromClassTrampoline>(module, "smoke_ChildClassFromClass")
        .def("__gluecodium_id__", [](const ChildClassFromClass& self) {
            return gluecodium::python::native_identity(self);
        })
        .def_static("__gluecodium_downcast__", [](const py::object& native) -> py::object {
            try {
                auto base = native.cast<std::shared_ptr<::smoke::ParentClass>>();
                auto derived = gluecodium::python::dynamic_pointer_cast<ChildClassFromClass>(base);
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
        .def(py::init([](std::shared_ptr<ChildClassFromClass> native) {
            auto self = std::make_shared<ChildClassFromClassTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("child_class_method", &ChildClassFromClass::child_class_method, py::call_guard<py::gil_scoped_release>())
        .def("root_method", &ChildClassFromClass::root_method, py::call_guard<py::gil_scoped_release>())
        .def_property("root_property", [](const ChildClassFromClass& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_root_property();
            });
        }, [](ChildClassFromClass& self, const ::std::string& value) {
            gluecodium::python::call_native([&] {
                self.set_root_property(value);
            });
        })
        ;


}
