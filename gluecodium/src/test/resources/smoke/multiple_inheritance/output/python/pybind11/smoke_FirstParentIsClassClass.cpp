

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
#include "smoke/FirstParentIsClassClass.h"
#include "smoke/ParentClass.h"
#include "smoke/ParentNarrowOne.h"
#include "string"

using FirstParentIsClassClass = ::smoke::FirstParentIsClassClass;

class FirstParentIsClassClassTrampoline : public FirstParentIsClassClass {
public:
    using FirstParentIsClassClass::FirstParentIsClassClass;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<FirstParentIsClassClass> m_impl;

    void child_function(
            /* no args */ ) override {
        if (m_impl) {
            m_impl->child_function();
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const FirstParentIsClassClass*>(this), "__gluecodium_callback_736d6f6b652e4669727374506172656e744973436c617373436c6173732e6368696c6446756e6374696f6e")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, FirstParentIsClassClass, "__gluecodium_callback_736d6f6b652e4669727374506172656e744973436c617373436c6173732e6368696c6446756e6374696f6e", child_function);
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsClassClass, child_function);
    }
    ::std::string get_child_property() const override {
        if (m_impl) {
            return m_impl->get_child_property();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const FirstParentIsClassClass*>(this), "__gluecodium_callback_736d6f6b652e4669727374506172656e744973436c617373436c6173732e6368696c6450726f7065727479_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, FirstParentIsClassClass, "__gluecodium_callback_736d6f6b652e4669727374506172656e744973436c617373436c6173732e6368696c6450726f7065727479_get", get_child_property);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsClassClass, get_child_property);
    }
    void set_child_property(const ::std::string& value) override {
        if (m_impl) {
            m_impl->set_child_property(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const FirstParentIsClassClass*>(this), "__gluecodium_callback_736d6f6b652e4669727374506172656e744973436c617373436c6173732e6368696c6450726f7065727479_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, FirstParentIsClassClass, "__gluecodium_callback_736d6f6b652e4669727374506172656e744973436c617373436c6173732e6368696c6450726f7065727479_set", set_child_property, value);
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsClassClass, set_child_property, value);
    }
    void parent_function(
            /* no args */ ) override {
        if (m_impl) {
            m_impl->parent_function();
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const FirstParentIsClassClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7446756e6374696f6e")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, FirstParentIsClassClass, "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7446756e6374696f6e", parent_function);
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsClassClass, parent_function);
    }
    void parent_function_one(
            /* no args */ ) override {
        if (m_impl) {
            m_impl->parent_function_one();
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const FirstParentIsClassClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7446756e6374696f6e4f6e65")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, FirstParentIsClassClass, "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7446756e6374696f6e4f6e65", parent_function_one);
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsClassClass, parent_function_one);
    }
    ::std::string get_parent_property() const override {
        if (m_impl) {
            return m_impl->get_parent_property();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const FirstParentIsClassClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7450726f7065727479_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, FirstParentIsClassClass, "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7450726f7065727479_get", get_parent_property);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsClassClass, get_parent_property);
    }
    void set_parent_property(const ::std::string& value) override {
        if (m_impl) {
            m_impl->set_parent_property(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const FirstParentIsClassClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7450726f7065727479_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, FirstParentIsClassClass, "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7450726f7065727479_set", set_parent_property, value);
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsClassClass, set_parent_property, value);
    }
    ::std::string get_parent_property_one() const override {
        if (m_impl) {
            return m_impl->get_parent_property_one();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const FirstParentIsClassClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7450726f70657274794f6e65_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, FirstParentIsClassClass, "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7450726f70657274794f6e65_get", get_parent_property_one);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsClassClass, get_parent_property_one);
    }
    void set_parent_property_one(const ::std::string& value) override {
        if (m_impl) {
            m_impl->set_parent_property_one(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const FirstParentIsClassClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7450726f70657274794f6e65_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, FirstParentIsClassClass, "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7450726f70657274794f6e65_set", set_parent_property_one, value);
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsClassClass, set_parent_property_one, value);
    }
};



void register_smoke_FirstParentIsClassClass(py::module_& module) {
auto cls_FirstParentIsClassClass = py::class_<FirstParentIsClassClass, ::smoke::ParentClass, ::smoke::ParentNarrowOne, std::shared_ptr<FirstParentIsClassClass>, FirstParentIsClassClassTrampoline>(module, "smoke_FirstParentIsClassClass", py::multiple_inheritance())
        .def("__gluecodium_id__", [](const FirstParentIsClassClass& self) {
            return gluecodium::python::native_identity(self);
        })
        .def_static("__gluecodium_downcast__", [](const py::object& native) -> py::object {
            try {
                auto base = native.cast<std::shared_ptr<::smoke::ParentClass>>();
                auto derived = gluecodium::python::dynamic_pointer_cast<FirstParentIsClassClass>(base);
                if (derived) return py::cast(derived);
            } catch (const py::cast_error&) {
            }
            try {
                auto base = native.cast<std::shared_ptr<::smoke::ParentNarrowOne>>();
                auto derived = gluecodium::python::dynamic_pointer_cast<FirstParentIsClassClass>(base);
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
        .def(py::init([](std::shared_ptr<FirstParentIsClassClass> native) {
            auto self = std::make_shared<FirstParentIsClassClassTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("child_function", &FirstParentIsClassClass::child_function, py::call_guard<py::gil_scoped_release>())
        .def_property("child_property", [](const FirstParentIsClassClass& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_child_property();
            });
        }, [](FirstParentIsClassClass& self, const ::std::string& value) {
            gluecodium::python::call_native([&] {
                self.set_child_property(value);
            });
        })
        .def("parent_function", &FirstParentIsClassClass::parent_function, py::call_guard<py::gil_scoped_release>())
        .def("parent_function_one", [](FirstParentIsClassClass& self) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.parent_function_one(); });
        })
        .def_property("parent_property", [](const FirstParentIsClassClass& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_parent_property();
            });
        }, [](FirstParentIsClassClass& self, const ::std::string& value) {
            gluecodium::python::call_native([&] {
                self.set_parent_property(value);
            });
        })
        .def_property("parent_property_one", [](const FirstParentIsClassClass& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_parent_property_one();
            });
        }, [](FirstParentIsClassClass& self, const ::std::string& value) {
            gluecodium::python::call_native([&] {
                self.set_parent_property_one(value);
            });
        })
        ;


}
