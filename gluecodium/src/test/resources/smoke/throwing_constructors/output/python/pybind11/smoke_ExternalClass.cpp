

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
#include "smoke/ExternalClass.h"
#include "cstdint"
#include "memory"

using ExternalClass = ::smoke::ExternalClass;
using InternalOne = ::smoke::ExternalClass::InternalOne;
using InternalTwo = ::smoke::ExternalClass::InternalTwo;
using ErrorEnum = ::smoke::ExternalClass::ErrorEnum;

class ExternalClassTrampoline : public ExternalClass {
public:
    using ExternalClass::ExternalClass;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ExternalClass> m_impl;

};



void register_smoke_ExternalClass(py::module_& module) {
auto cls_ExternalClass = py::class_<ExternalClass, std::shared_ptr<ExternalClass>, ExternalClassTrampoline>(module, "smoke_ExternalClass")
        .def("__gluecodium_id__", [](const ExternalClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<ExternalClass> native) {
            auto self = std::make_shared<ExternalClassTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def_static("create", &ExternalClass::create)
        ;

auto cls_ExternalClassInternalOne = py::class_<InternalOne, std::shared_ptr<InternalOne>>(cls_ExternalClass, "InternalOne")
        .def("__gluecodium_id__", [](const InternalOne& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("create", py::overload_cast<>(InternalOne::create))
        .def_static("create", py::overload_cast<const uint64_t>(InternalOne::create), py::arg("value"))
        ;

auto cls_ExternalClassInternalTwo = py::class_<InternalTwo, std::shared_ptr<InternalTwo>>(cls_ExternalClass, "InternalTwo")
        .def("__gluecodium_id__", [](const InternalTwo& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("create", &InternalTwo::create)
        ;

auto cls_ExternalClassErrorEnum = py::enum_<ErrorEnum>(cls_ExternalClass, "ErrorEnum")
        .value("NONE", ErrorEnum::NONE)
        .value("CRASHED", ErrorEnum::CRASHED)
        ;

    static py::exception<::std::error_code> exc_ConstructorExplodedError(cls_ExternalClass, "ConstructorExplodedError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::error_code& e) {
            PyErr_SetString(exc_ConstructorExplodedError.ptr(), e.message().c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::error_code>(exc_ConstructorExplodedError.ptr());


}
