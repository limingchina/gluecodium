

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
#include "smoke/DeprecationCommentsOnly.h"
#include "string"

using DeprecationCommentsOnly = ::smoke::DeprecationCommentsOnly;
using SomeStruct = ::smoke::DeprecationCommentsOnly::SomeStruct;
using SomeEnum = ::smoke::DeprecationCommentsOnly::SomeEnum;

class DeprecationCommentsOnlyTrampoline : public DeprecationCommentsOnly {
public:
    using DeprecationCommentsOnly::DeprecationCommentsOnly;
    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<DeprecationCommentsOnly> m_impl;

    bool some_method_with_all_comments(
            const ::std::string& input ) override {
        if (m_impl) {
            return m_impl->some_method_with_all_comments(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const DeprecationCommentsOnly*>(this), "__gluecodium_callback_736d6f6b652e4465707265636174696f6e436f6d6d656e74734f6e6c792e736f6d654d6574686f6457697468416c6c436f6d6d656e7473")) {
        PYBIND11_OVERRIDE_PURE_NAME(bool, DeprecationCommentsOnly, "__gluecodium_callback_736d6f6b652e4465707265636174696f6e436f6d6d656e74734f6e6c792e736f6d654d6574686f6457697468416c6c436f6d6d656e7473", some_method_with_all_comments, input);
        }
        PYBIND11_OVERRIDE_PURE(bool, DeprecationCommentsOnly, some_method_with_all_comments, input);
    }
    bool is_some_property() const override {
        if (m_impl) {
            return m_impl->is_some_property();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const DeprecationCommentsOnly*>(this), "__gluecodium_callback_736d6f6b652e4465707265636174696f6e436f6d6d656e74734f6e6c792e536f6d6550726f7065727479_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(bool, DeprecationCommentsOnly, "__gluecodium_callback_736d6f6b652e4465707265636174696f6e436f6d6d656e74734f6e6c792e536f6d6550726f7065727479_get", is_some_property);
        }
        PYBIND11_OVERRIDE_PURE(bool, DeprecationCommentsOnly, is_some_property);
    }
    void set_some_property(const bool value) override {
        if (m_impl) {
            m_impl->set_some_property(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const DeprecationCommentsOnly*>(this), "__gluecodium_callback_736d6f6b652e4465707265636174696f6e436f6d6d656e74734f6e6c792e536f6d6550726f7065727479_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, DeprecationCommentsOnly, "__gluecodium_callback_736d6f6b652e4465707265636174696f6e436f6d6d656e74734f6e6c792e536f6d6550726f7065727479_set", set_some_property, value);
        }
        PYBIND11_OVERRIDE_PURE(void, DeprecationCommentsOnly, set_some_property, value);
    }
};



void register_smoke_DeprecationCommentsOnly(py::module_& module) {
auto cls_DeprecationCommentsOnly = py::class_<DeprecationCommentsOnly, std::shared_ptr<DeprecationCommentsOnly>, DeprecationCommentsOnlyTrampoline>(module, "smoke_DeprecationCommentsOnly")
        .def("__gluecodium_id__", [](const DeprecationCommentsOnly& self) {
            return gluecodium::python::native_identity(self);
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<DeprecationCommentsOnly> native) {
            auto self = std::make_shared<DeprecationCommentsOnlyTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("some_method_with_all_comments", [](DeprecationCommentsOnly& self, const ::std::string& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.some_method_with_all_comments(input); });
        }, py::arg("input"))
        .def_property("is_some_property", [](const DeprecationCommentsOnly& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.is_some_property();
            });
        }, [](DeprecationCommentsOnly& self, const bool value) {
            gluecodium::python::call_native([&] {
                self.set_some_property(value);
            });
        })
        ;

auto cls_DeprecationCommentsOnlySomeStruct = py::class_<SomeStruct>(cls_DeprecationCommentsOnly, "SomeStruct")
        .def_property("some_field", [](const SomeStruct& self) -> decltype(auto) {
            return
                (self.some_field)
            ;
        }, [](SomeStruct& self, const bool value) {

                self.some_field = value;

        })
        .def(py::init<>())
        .def(py::init<bool>(), py::arg("some_field"))
        ;

auto cls_DeprecationCommentsOnlySomeEnum = py::enum_<SomeEnum>(cls_DeprecationCommentsOnly, "SomeEnum")
        .value("USELESS", SomeEnum::USELESS)
        ;


}
