

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
#include "smoke/ParentInterface.h"
#include "memory"
#include "string"

using ParentInterface = ::smoke::ParentInterface;

class ParentInterfaceTrampoline : public ParentInterface {
public:
    using ParentInterface::ParentInterface;
    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ParentInterface> m_impl;

    void parent_function(
            /* no args */ ) override {
        if (m_impl) {
            m_impl->parent_function();
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ParentInterface*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e706172656e7446756e6374696f6e")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, ParentInterface, "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e706172656e7446756e6374696f6e", parent_function);
        }
        PYBIND11_OVERRIDE_PURE(void, ParentInterface, parent_function);
    }
    void some_function_that_uses_type_from_another_package(
            const ::std::shared_ptr< ::another::SomeCoolClassType >& some_param ) override {
        if (m_impl) {
            m_impl->some_function_that_uses_type_from_another_package(some_param);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ParentInterface*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e736f6d655f66756e6374696f6e5f746861745f757365735f747970655f66726f6d5f616e6f746865725f7061636b616765")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, ParentInterface, "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e736f6d655f66756e6374696f6e5f746861745f757365735f747970655f66726f6d5f616e6f746865725f7061636b616765", some_function_that_uses_type_from_another_package, some_param);
        }
        PYBIND11_OVERRIDE_PURE(void, ParentInterface, some_function_that_uses_type_from_another_package, some_param);
    }
    ::std::string get_parent_property() const override {
        if (m_impl) {
            return m_impl->get_parent_property();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ParentInterface*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e706172656e7450726f7065727479_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, ParentInterface, "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e706172656e7450726f7065727479_get", get_parent_property);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, ParentInterface, get_parent_property);
    }
    void set_parent_property(const ::std::string& value) override {
        if (m_impl) {
            m_impl->set_parent_property(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ParentInterface*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e706172656e7450726f7065727479_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, ParentInterface, "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e706172656e7450726f7065727479_set", set_parent_property, value);
        }
        PYBIND11_OVERRIDE_PURE(void, ParentInterface, set_parent_property, value);
    }
};



void register_smoke_ParentInterface(py::module_& module) {
auto cls_ParentInterface = py::class_<ParentInterface, std::shared_ptr<ParentInterface>, ParentInterfaceTrampoline>(module, "smoke_ParentInterface")
        .def("__gluecodium_id__", [](const ParentInterface& self) {
            return gluecodium::python::native_identity(self);
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<ParentInterface> native) {
            auto self = std::make_shared<ParentInterfaceTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("parent_function", [](ParentInterface& self) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.parent_function(); });
        })
        .def("some_function_that_uses_type_from_another_package", [](ParentInterface& self, const ::std::shared_ptr< ::another::SomeCoolClassType >& some_param) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.some_function_that_uses_type_from_another_package(some_param); });
        }, py::arg("some_param"))
        .def_property("parent_property", [](const ParentInterface& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_parent_property();
            });
        }, [](ParentInterface& self, const ::std::string& value) {
            gluecodium::python::call_native([&] {
                self.set_parent_property(value);
            });
        })
        ;


}
