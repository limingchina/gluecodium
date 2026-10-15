

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
#include "smoke/DeprecationComments.h"
#include "string"

using DeprecationComments = ::smoke::DeprecationComments;
using SomeStruct = ::smoke::DeprecationComments::SomeStruct;
using SomeEnum = ::smoke::DeprecationComments::SomeEnum;

class DeprecationCommentsTrampoline : public DeprecationComments {
public:
    using DeprecationComments::DeprecationComments;
    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<DeprecationComments> m_impl;

    bool some_method_with_all_comments(
            const ::std::string& input ) override {
        if (m_impl) {
            return m_impl->some_method_with_all_comments(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const DeprecationComments*>(this), "__gluecodium_callback_736d6f6b652e4465707265636174696f6e436f6d6d656e74732e736f6d654d6574686f6457697468416c6c436f6d6d656e7473")) {
        PYBIND11_OVERRIDE_PURE_NAME(bool, DeprecationComments, "__gluecodium_callback_736d6f6b652e4465707265636174696f6e436f6d6d656e74732e736f6d654d6574686f6457697468416c6c436f6d6d656e7473", some_method_with_all_comments, input);
        }
        PYBIND11_OVERRIDE_PURE(bool, DeprecationComments, some_method_with_all_comments, input);
    }
    bool is_some_property() const override {
        if (m_impl) {
            return m_impl->is_some_property();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const DeprecationComments*>(this), "__gluecodium_callback_736d6f6b652e4465707265636174696f6e436f6d6d656e74732e536f6d6550726f7065727479_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(bool, DeprecationComments, "__gluecodium_callback_736d6f6b652e4465707265636174696f6e436f6d6d656e74732e536f6d6550726f7065727479_get", is_some_property);
        }
        PYBIND11_OVERRIDE_PURE(bool, DeprecationComments, is_some_property);
    }
    void set_some_property(const bool value) override {
        if (m_impl) {
            m_impl->set_some_property(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const DeprecationComments*>(this), "__gluecodium_callback_736d6f6b652e4465707265636174696f6e436f6d6d656e74732e536f6d6550726f7065727479_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, DeprecationComments, "__gluecodium_callback_736d6f6b652e4465707265636174696f6e436f6d6d656e74732e536f6d6550726f7065727479_set", set_some_property, value);
        }
        PYBIND11_OVERRIDE_PURE(void, DeprecationComments, set_some_property, value);
    }
    ::std::string get_property_but_not_accessors() const override {
        if (m_impl) {
            return m_impl->get_property_but_not_accessors();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const DeprecationComments*>(this), "__gluecodium_callback_736d6f6b652e4465707265636174696f6e436f6d6d656e74732e50726f70657274794275744e6f744163636573736f7273_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, DeprecationComments, "__gluecodium_callback_736d6f6b652e4465707265636174696f6e436f6d6d656e74732e50726f70657274794275744e6f744163636573736f7273_get", get_property_but_not_accessors);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, DeprecationComments, get_property_but_not_accessors);
    }
    void set_property_but_not_accessors(const ::std::string& value) override {
        if (m_impl) {
            m_impl->set_property_but_not_accessors(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const DeprecationComments*>(this), "__gluecodium_callback_736d6f6b652e4465707265636174696f6e436f6d6d656e74732e50726f70657274794275744e6f744163636573736f7273_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, DeprecationComments, "__gluecodium_callback_736d6f6b652e4465707265636174696f6e436f6d6d656e74732e50726f70657274794275744e6f744163636573736f7273_set", set_property_but_not_accessors, value);
        }
        PYBIND11_OVERRIDE_PURE(void, DeprecationComments, set_property_but_not_accessors, value);
    }
};



void register_smoke_DeprecationComments(py::module_& module) {
auto cls_DeprecationComments = py::class_<DeprecationComments, std::shared_ptr<DeprecationComments>, DeprecationCommentsTrampoline>(module, "smoke_DeprecationComments")
        .def("__gluecodium_id__", [](const DeprecationComments& self) {
            return gluecodium::python::native_identity(self);
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<DeprecationComments> native) {
            auto self = std::make_shared<DeprecationCommentsTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("some_method_with_all_comments", [](DeprecationComments& self, const ::std::string& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.some_method_with_all_comments(input); });
        }, py::arg("input"))
        .def_property("is_some_property", [](const DeprecationComments& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.is_some_property();
            });
        }, [](DeprecationComments& self, const bool value) {
            gluecodium::python::call_native([&] {
                self.set_some_property(value);
            });
        })
        .def_property("property_but_not_accessors", [](const DeprecationComments& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_property_but_not_accessors();
            });
        }, [](DeprecationComments& self, const ::std::string& value) {
            gluecodium::python::call_native([&] {
                self.set_property_but_not_accessors(value);
            });
        })
        ;

auto cls_DeprecationCommentsSomeStruct = py::class_<SomeStruct>(cls_DeprecationComments, "SomeStruct")
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

auto cls_DeprecationCommentsSomeEnum = py::enum_<SomeEnum>(cls_DeprecationComments, "SomeEnum")
        .value("USELESS", SomeEnum::USELESS)
        ;

    static py::exception<::std::error_code> exc_SomethingWrongError(cls_DeprecationComments, "SomethingWrongError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::error_code& e) {
            PyErr_SetString(exc_SomethingWrongError.ptr(), e.message().c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::error_code>(exc_SomethingWrongError.ptr());


}
