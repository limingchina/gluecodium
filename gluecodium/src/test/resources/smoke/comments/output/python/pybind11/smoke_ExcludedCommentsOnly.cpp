

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
            return gluecodium::python::native_identity(self);
        })
        .def("some_method_with_all_comments", &ExcludedCommentsOnly::some_method_with_all_comments, py::arg("input_parameter"), py::call_guard<py::gil_scoped_release>())
        .def("some_method_without_return_type_or_input_parameters", &ExcludedCommentsOnly::some_method_without_return_type_or_input_parameters, py::call_guard<py::gil_scoped_release>())
        .def_property("is_some_property", [](const ExcludedCommentsOnly& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.is_some_property();
            });
        }, [](ExcludedCommentsOnly& self, const bool value) {
            gluecodium::python::call_native([&] {
                self.set_some_property(value);
            });
        })
        ;

auto cls_ExcludedCommentsOnlySomeStruct = py::class_<SomeStruct>(cls_ExcludedCommentsOnly, "SomeStruct")
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
