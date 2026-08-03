

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

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
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->some_method_with_all_comments(input);
        }
        PYBIND11_OVERRIDE_PURE(bool, DeprecationComments, some_method_with_all_comments, input);
    }
    bool is_some_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->is_some_property();
        }
        PYBIND11_OVERRIDE_PURE(bool, DeprecationComments, is_some_property);
    }
    void set_some_property(const bool value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_some_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, DeprecationComments, set_some_property, value);
    }
    ::std::string get_property_but_not_accessors() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_property_but_not_accessors();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, DeprecationComments, get_property_but_not_accessors);
    }
    void set_property_but_not_accessors(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_property_but_not_accessors(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, DeprecationComments, set_property_but_not_accessors, value);
    }
};



void register_smoke_DeprecationComments(py::module_& module) {
auto cls_DeprecationComments = py::class_<DeprecationComments, std::shared_ptr<DeprecationComments>, DeprecationCommentsTrampoline>(module, "smoke_DeprecationComments")
        .def("__gluecodium_id__", [](const DeprecationComments& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
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
            return self.some_method_with_all_comments(input);
        }, py::arg("input"))
        .def_property("is_some_property", [](const DeprecationComments& self) {
            return self.is_some_property();
        }, [](DeprecationComments& self, const bool value) {
            self.set_some_property(value);
        })
        .def_property("property_but_not_accessors", [](const DeprecationComments& self) {
            return self.get_property_but_not_accessors();
        }, [](DeprecationComments& self, const ::std::string& value) {
            self.set_property_but_not_accessors(value);
        })
        ;

auto cls_DeprecationCommentsSomeStruct = py::class_<SomeStruct>(cls_DeprecationComments, "SomeStruct")
        .def_readwrite("some_field", &SomeStruct::some_field)
        .def(py::init<>())
        .def(py::init<bool>(), py::arg("some_field"))
        ;

auto cls_DeprecationCommentsSomeEnum = py::enum_<SomeEnum>(cls_DeprecationComments, "SomeEnum")
        .value("USELESS", SomeEnum::USELESS)
        ;

    static py::exception<::std::error_code> exc(cls_DeprecationComments, "SomethingWrongError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::error_code& e) {
            PyErr_SetString(exc.ptr(), e.message().c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::error_code>(exc.ptr());


}
