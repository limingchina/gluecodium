

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
#include "smoke/ExcludedComments.h"
#include "cstdint"
#include "functional"
#include "string"

using ExcludedComments = ::smoke::ExcludedComments;
using SomeStruct = ::smoke::ExcludedComments::SomeStruct;
using SomeEnum = ::smoke::ExcludedComments::SomeEnum;



void register_smoke_ExcludedComments(py::module_& module) {
auto cls_ExcludedComments = py::class_<ExcludedComments, std::shared_ptr<ExcludedComments>>(module, "smoke_ExcludedComments")
        .def("__gluecodium_id__", [](const ExcludedComments& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("some_method_with_all_comments", &ExcludedComments::some_method_with_all_comments, py::arg("input_parameter"))
        .def("some_method_without_return_type_or_input_parameters", &ExcludedComments::some_method_without_return_type_or_input_parameters)
        .def_property("is_some_property", py::overload_cast<>(&ExcludedComments::is_some_property, py::const_), py::overload_cast<const bool>(&ExcludedComments::set_some_property))
        ;

auto cls_ExcludedCommentsSomeStruct = py::class_<SomeStruct>(cls_ExcludedComments, "SomeStruct")
        .def_readwrite("some_field", &SomeStruct::some_field)
        .def(py::init<>())
        .def(py::init<bool>(), py::arg("some_field"))
        ;

auto cls_ExcludedCommentsSomeEnum = py::enum_<SomeEnum>(cls_ExcludedComments, "SomeEnum")
        .value("USELESS", SomeEnum::USELESS)
        ;

    static py::exception<::std::error_code> exc_SomethingWrongError(cls_ExcludedComments, "SomethingWrongError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::error_code& e) {
            PyErr_SetString(exc_SomethingWrongError.ptr(), e.message().c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::error_code>(exc_SomethingWrongError.ptr());


}
