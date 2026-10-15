

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
            return gluecodium::python::native_identity(self);
        })
        .def("some_method_with_all_comments", &ExcludedComments::some_method_with_all_comments, py::arg("input_parameter"), py::call_guard<py::gil_scoped_release>())
        .def("some_method_without_return_type_or_input_parameters", &ExcludedComments::some_method_without_return_type_or_input_parameters, py::call_guard<py::gil_scoped_release>())
        .def_property("is_some_property", [](const ExcludedComments& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.is_some_property();
            });
        }, [](ExcludedComments& self, const bool value) {
            gluecodium::python::call_native([&] {
                self.set_some_property(value);
            });
        })
        ;

auto cls_ExcludedCommentsSomeStruct = py::class_<SomeStruct>(cls_ExcludedComments, "SomeStruct")
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
