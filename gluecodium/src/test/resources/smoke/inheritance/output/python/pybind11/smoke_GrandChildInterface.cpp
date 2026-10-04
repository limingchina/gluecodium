

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
#include "smoke/ChildInterface.h"
#include "smoke/GrandChildInterface.h"

using GrandChildInterface = ::smoke::GrandChildInterface;

class GrandChildInterfaceTrampoline : public GrandChildInterface {
public:
    using GrandChildInterface::GrandChildInterface;
    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<GrandChildInterface> m_impl;

    void grand_child_method(
            /* no args */ ) override {
        if (m_impl) {
            m_impl->grand_child_method();
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const GrandChildInterface*>(this), "__gluecodium_callback_736d6f6b652e4772616e644368696c64496e746572666163652e6772616e644368696c644d6574686f64")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, GrandChildInterface, "__gluecodium_callback_736d6f6b652e4772616e644368696c64496e746572666163652e6772616e644368696c644d6574686f64", grand_child_method);
        }
        PYBIND11_OVERRIDE_PURE(void, GrandChildInterface, grand_child_method);
    }
    void child_method(
            /* no args */ ) override {
        if (m_impl) {
            m_impl->child_method();
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const GrandChildInterface*>(this), "__gluecodium_callback_736d6f6b652e4368696c64496e746572666163652e6368696c644d6574686f64")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, GrandChildInterface, "__gluecodium_callback_736d6f6b652e4368696c64496e746572666163652e6368696c644d6574686f64", child_method);
        }
        PYBIND11_OVERRIDE_PURE(void, GrandChildInterface, child_method);
    }
    void root_method(
            /* no args */ ) override {
        if (m_impl) {
            m_impl->root_method();
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const GrandChildInterface*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f744d6574686f64")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, GrandChildInterface, "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f744d6574686f64", root_method);
        }
        PYBIND11_OVERRIDE_PURE(void, GrandChildInterface, root_method);
    }
    ::std::string get_root_property() const override {
        if (m_impl) {
            return m_impl->get_root_property();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const GrandChildInterface*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f7450726f7065727479_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, GrandChildInterface, "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f7450726f7065727479_get", get_root_property);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, GrandChildInterface, get_root_property);
    }
    void set_root_property(const ::std::string& value) override {
        if (m_impl) {
            m_impl->set_root_property(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const GrandChildInterface*>(this), "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f7450726f7065727479_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, GrandChildInterface, "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f7450726f7065727479_set", set_root_property, value);
        }
        PYBIND11_OVERRIDE_PURE(void, GrandChildInterface, set_root_property, value);
    }
};



void register_smoke_GrandChildInterface(py::module_& module) {
auto cls_GrandChildInterface = py::class_<GrandChildInterface, ::smoke::ChildInterface, std::shared_ptr<GrandChildInterface>, GrandChildInterfaceTrampoline>(module, "smoke_GrandChildInterface")
        .def("__gluecodium_id__", [](const GrandChildInterface& self) {
            return gluecodium::python::native_identity(self);
        })
        .def_static("__gluecodium_downcast__", [](const py::object& native) -> py::object {
            try {
                auto base = native.cast<std::shared_ptr<::smoke::ChildInterface>>();
                auto derived = gluecodium::python::dynamic_pointer_cast<GrandChildInterface>(base);
                if (derived) return py::cast(derived);
            } catch (const py::cast_error&) {
            }
            try {
                auto base = native.cast<std::shared_ptr<::smoke::ParentInterface>>();
                auto derived = gluecodium::python::dynamic_pointer_cast<GrandChildInterface>(base);
                if (derived) return py::cast(derived);
            } catch (const py::cast_error&) {
            }
            return py::none();
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<GrandChildInterface> native) {
            auto self = std::make_shared<GrandChildInterfaceTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("grand_child_method", [](GrandChildInterface& self) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.grand_child_method(); });
        })
        .def("child_method", [](GrandChildInterface& self) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.child_method(); });
        })
        .def("root_method", [](GrandChildInterface& self) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.root_method(); });
        })
        .def_property("root_property", [](const GrandChildInterface& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_root_property();
            });
        }, [](GrandChildInterface& self, const ::std::string& value) {
            gluecodium::python::call_native([&] {
                self.set_root_property(value);
            });
        })
        ;


}
