

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
#include "smoke/ExcludedCommentsOnly.h"
#include "cstdint"
#include "functional"
#include "string"

using ExcludedCommentsOnly = ::smoke::ExcludedCommentsOnly;
using SomeStruct = ::smoke::ExcludedCommentsOnly::SomeStruct;
using SomeEnum = ::smoke::ExcludedCommentsOnly::SomeEnum;



void register_smoke_ExcludedCommentsOnly(py::module_& module) {
auto cls_ExcludedCommentsOnly = py::class_<ExcludedCommentsOnly, std::shared_ptr<ExcludedCommentsOnly>>(module, "smoke_ExcludedCommentsOnly")
        .def("__gluecodium_id__", [](const ExcludedCommentsOnly& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("some_method_with_all_comments", &ExcludedCommentsOnly::some_method_with_all_comments, py::arg("input_parameter"))
        .def("some_method_without_return_type_or_input_parameters", &ExcludedCommentsOnly::some_method_without_return_type_or_input_parameters)
        .def_property("is_some_property", py::overload_cast<>(&ExcludedCommentsOnly::is_some_property, py::const_), py::overload_cast<const bool>(&ExcludedCommentsOnly::set_some_property))
        ;

auto cls_ExcludedCommentsOnlySomeStruct = py::class_<SomeStruct>(cls_ExcludedCommentsOnly, "SomeStruct")
        .def_readwrite("some_field", &SomeStruct::some_field)
        .def(py::init<>())
        .def(py::init<bool>(), py::arg("some_field"))
        ;

auto cls_ExcludedCommentsOnlySomeEnum = py::enum_<SomeEnum>(cls_ExcludedCommentsOnly, "SomeEnum")
        .value("USELESS", SomeEnum::USELESS)
        ;

    static py::exception<::std::error_code> exc_SomethingWrongError(cls_ExcludedCommentsOnly, "SomethingWrongError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::error_code& e) {
            PyErr_SetString(exc_SomethingWrongError.ptr(), e.message().c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::error_code>(exc_SomethingWrongError.ptr());


}
