

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
#include "another/SomeCoolClassType.h"
#include "smoke/FirstParentIsInterfaceClass.h"
#include "smoke/ParentInterface.h"
#include "smoke/ParentNarrowOne.h"
#include "memory"
#include "string"

using FirstParentIsInterfaceClass = ::smoke::FirstParentIsInterfaceClass;

class FirstParentIsInterfaceClassTrampoline : public FirstParentIsInterfaceClass {
public:
    using FirstParentIsInterfaceClass::FirstParentIsInterfaceClass;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<FirstParentIsInterfaceClass> m_impl;

    void child_function(
            /* no args */ ) override {
        if (m_impl) {
            m_impl->child_function();
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const FirstParentIsInterfaceClass*>(this), "__gluecodium_callback_736d6f6b652e4669727374506172656e744973496e74657266616365436c6173732e6368696c6446756e6374696f6e")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, FirstParentIsInterfaceClass, "__gluecodium_callback_736d6f6b652e4669727374506172656e744973496e74657266616365436c6173732e6368696c6446756e6374696f6e", child_function);
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceClass, child_function);
    }
    ::std::string get_child_property() const override {
        if (m_impl) {
            return m_impl->get_child_property();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const FirstParentIsInterfaceClass*>(this), "__gluecodium_callback_736d6f6b652e4669727374506172656e744973496e74657266616365436c6173732e6368696c6450726f7065727479_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, FirstParentIsInterfaceClass, "__gluecodium_callback_736d6f6b652e4669727374506172656e744973496e74657266616365436c6173732e6368696c6450726f7065727479_get", get_child_property);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsInterfaceClass, get_child_property);
    }
    void set_child_property(const ::std::string& value) override {
        if (m_impl) {
            m_impl->set_child_property(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const FirstParentIsInterfaceClass*>(this), "__gluecodium_callback_736d6f6b652e4669727374506172656e744973496e74657266616365436c6173732e6368696c6450726f7065727479_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, FirstParentIsInterfaceClass, "__gluecodium_callback_736d6f6b652e4669727374506172656e744973496e74657266616365436c6173732e6368696c6450726f7065727479_set", set_child_property, value);
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceClass, set_child_property, value);
    }
    void parent_function(
            /* no args */ ) override {
        if (m_impl) {
            m_impl->parent_function();
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const FirstParentIsInterfaceClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e706172656e7446756e6374696f6e")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, FirstParentIsInterfaceClass, "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e706172656e7446756e6374696f6e", parent_function);
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceClass, parent_function);
    }
    void some_function_that_uses_type_from_another_package(
            const ::std::shared_ptr< ::another::SomeCoolClassType >& some_param ) override {
        if (m_impl) {
            m_impl->some_function_that_uses_type_from_another_package(some_param);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const FirstParentIsInterfaceClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e736f6d655f66756e6374696f6e5f746861745f757365735f747970655f66726f6d5f616e6f746865725f7061636b616765")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, FirstParentIsInterfaceClass, "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e736f6d655f66756e6374696f6e5f746861745f757365735f747970655f66726f6d5f616e6f746865725f7061636b616765", some_function_that_uses_type_from_another_package, some_param);
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceClass, some_function_that_uses_type_from_another_package, some_param);
    }
    void parent_function_one(
            /* no args */ ) override {
        if (m_impl) {
            m_impl->parent_function_one();
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const FirstParentIsInterfaceClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7446756e6374696f6e4f6e65")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, FirstParentIsInterfaceClass, "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7446756e6374696f6e4f6e65", parent_function_one);
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceClass, parent_function_one);
    }
    ::std::string get_parent_property() const override {
        if (m_impl) {
            return m_impl->get_parent_property();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const FirstParentIsInterfaceClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e706172656e7450726f7065727479_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, FirstParentIsInterfaceClass, "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e706172656e7450726f7065727479_get", get_parent_property);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsInterfaceClass, get_parent_property);
    }
    void set_parent_property(const ::std::string& value) override {
        if (m_impl) {
            m_impl->set_parent_property(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const FirstParentIsInterfaceClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e706172656e7450726f7065727479_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, FirstParentIsInterfaceClass, "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e706172656e7450726f7065727479_set", set_parent_property, value);
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceClass, set_parent_property, value);
    }
    ::std::string get_parent_property_one() const override {
        if (m_impl) {
            return m_impl->get_parent_property_one();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const FirstParentIsInterfaceClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7450726f70657274794f6e65_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, FirstParentIsInterfaceClass, "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7450726f70657274794f6e65_get", get_parent_property_one);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsInterfaceClass, get_parent_property_one);
    }
    void set_parent_property_one(const ::std::string& value) override {
        if (m_impl) {
            m_impl->set_parent_property_one(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const FirstParentIsInterfaceClass*>(this), "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7450726f70657274794f6e65_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, FirstParentIsInterfaceClass, "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7450726f70657274794f6e65_set", set_parent_property_one, value);
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceClass, set_parent_property_one, value);
    }
};



void register_smoke_FirstParentIsInterfaceClass(py::module_& module) {
auto cls_FirstParentIsInterfaceClass = py::class_<FirstParentIsInterfaceClass, ::smoke::ParentInterface, ::smoke::ParentNarrowOne, std::shared_ptr<FirstParentIsInterfaceClass>, FirstParentIsInterfaceClassTrampoline>(module, "smoke_FirstParentIsInterfaceClass", py::multiple_inheritance())
        .def("__gluecodium_id__", [](const FirstParentIsInterfaceClass& self) {
            return gluecodium::python::native_identity(self);
        })
        .def_static("__gluecodium_downcast__", [](const py::object& native) -> py::object {
            try {
                auto base = native.cast<std::shared_ptr<::smoke::ParentInterface>>();
                auto derived = gluecodium::python::dynamic_pointer_cast<FirstParentIsInterfaceClass>(base);
                if (derived) return py::cast(derived);
            } catch (const py::cast_error&) {
            }
            try {
                auto base = native.cast<std::shared_ptr<::smoke::ParentNarrowOne>>();
                auto derived = gluecodium::python::dynamic_pointer_cast<FirstParentIsInterfaceClass>(base);
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
        .def(py::init([](std::shared_ptr<FirstParentIsInterfaceClass> native) {
            auto self = std::make_shared<FirstParentIsInterfaceClassTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("child_function", &FirstParentIsInterfaceClass::child_function, py::call_guard<py::gil_scoped_release>())
        .def_property("child_property", [](const FirstParentIsInterfaceClass& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_child_property();
            });
        }, [](FirstParentIsInterfaceClass& self, const ::std::string& value) {
            gluecodium::python::call_native([&] {
                self.set_child_property(value);
            });
        })
        .def("parent_function", [](FirstParentIsInterfaceClass& self) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.parent_function(); });
        })
        .def("some_function_that_uses_type_from_another_package", [](FirstParentIsInterfaceClass& self, const ::std::shared_ptr< ::another::SomeCoolClassType >& some_param) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.some_function_that_uses_type_from_another_package(some_param); });
        }, py::arg("some_param"))
        .def("parent_function_one", [](FirstParentIsInterfaceClass& self) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.parent_function_one(); });
        })
        .def_property("parent_property", [](const FirstParentIsInterfaceClass& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_parent_property();
            });
        }, [](FirstParentIsInterfaceClass& self, const ::std::string& value) {
            gluecodium::python::call_native([&] {
                self.set_parent_property(value);
            });
        })
        .def_property("parent_property_one", [](const FirstParentIsInterfaceClass& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_parent_property_one();
            });
        }, [](FirstParentIsInterfaceClass& self, const ::std::string& value) {
            gluecodium::python::call_native([&] {
                self.set_parent_property_one(value);
            });
        })
        ;


}
