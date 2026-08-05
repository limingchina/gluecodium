

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
#include "gluecodium/VectorHash.h"
#include "package/Types.h"
#include "vector"

using Types = ::package::Types;
using Struct = ::package::Types::Struct;
using Enum = ::package::Types::Enum;



void register_package_Types(py::module_& module) {
auto cls_Types = py::class_<Types>(module, "package_Types")
        .def(py::init<>())
        ;

auto cls_typesstruct = py::class_<Struct>(cls_Types, "Struct")
        .def_readwrite("null", &Struct::null)
        .def(py::init<>())
        .def(py::init<::package::Types::Enum>(), py::arg("null"))
        ;

auto cls_typesenum = py::enum_<Enum>(cls_Types, "Enum")
        .value("NA_N", Enum::NA_N)
        ;

    static py::exception<::std::error_code> exc_ExceptionError(cls_Types, "ExceptionError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::error_code& e) {
            PyErr_SetString(exc_ExceptionError.ptr(), e.message().c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::error_code>(exc_ExceptionError.ptr());


}
