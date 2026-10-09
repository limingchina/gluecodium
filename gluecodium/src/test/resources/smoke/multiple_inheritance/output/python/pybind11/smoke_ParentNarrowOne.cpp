

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
#include "smoke/ParentNarrowOne.h"
#include "string"

using ParentNarrowOne = ::smoke::ParentNarrowOne;

class ParentNarrowOneTrampoline : public ParentNarrowOne {
public:
    using ParentNarrowOne::ParentNarrowOne;
    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ParentNarrowOne> m_impl;

    void parent_function_one(
            /* no args */ ) override {
        if (m_impl) {
            m_impl->parent_function_one();
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ParentNarrowOne*>(this), "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7446756e6374696f6e4f6e65")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, ParentNarrowOne, "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7446756e6374696f6e4f6e65", parent_function_one);
        }
        PYBIND11_OVERRIDE_PURE(void, ParentNarrowOne, parent_function_one);
    }
    ::std::string get_parent_property_one() const override {
        if (m_impl) {
            return m_impl->get_parent_property_one();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ParentNarrowOne*>(this), "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7450726f70657274794f6e65_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, ParentNarrowOne, "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7450726f70657274794f6e65_get", get_parent_property_one);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, ParentNarrowOne, get_parent_property_one);
    }
    void set_parent_property_one(const ::std::string& value) override {
        if (m_impl) {
            m_impl->set_parent_property_one(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const ParentNarrowOne*>(this), "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7450726f70657274794f6e65_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, ParentNarrowOne, "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7450726f70657274794f6e65_set", set_parent_property_one, value);
        }
        PYBIND11_OVERRIDE_PURE(void, ParentNarrowOne, set_parent_property_one, value);
    }
};



void register_smoke_ParentNarrowOne(py::module_& module) {
auto cls_ParentNarrowOne = py::class_<ParentNarrowOne, std::shared_ptr<ParentNarrowOne>, ParentNarrowOneTrampoline>(module, "smoke_ParentNarrowOne")
        .def("__gluecodium_id__", [](const ParentNarrowOne& self) {
            return gluecodium::python::native_identity(self);
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<ParentNarrowOne> native) {
            auto self = std::make_shared<ParentNarrowOneTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("parent_function_one", [](ParentNarrowOne& self) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.parent_function_one(); });
        })
        .def_property("parent_property_one", [](const ParentNarrowOne& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_parent_property_one();
            });
        }, [](ParentNarrowOne& self, const ::std::string& value) {
            gluecodium::python::call_native([&] {
                self.set_parent_property_one(value);
            });
        })
        ;


}
