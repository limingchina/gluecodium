

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
#include "gluecodium/TimePointHash.h"
#include "smoke/Dates.h"
#include "chrono"
#include "optional"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DateStruct = ::smoke::Dates::DateStruct;

void register_smoke_DatesDateStruct(py::module_& module) {
    py::class_<DateStruct>(module, "smoke_DatesDateStruct")
        .def_readwrite("date_field", &DateStruct::date_field)
        .def_readwrite("nullable_date_field", &DateStruct::nullable_date_field)
        .def(py::init<>())
        .def(py::init<::std::chrono::system_clock::time_point>(), py::arg("date_field"))
        .def(py::init<::std::chrono::system_clock::time_point, std::optional< ::std::chrono::system_clock::time_point >>(), py::arg("date_field"), py::arg("nullable_date_field"))
        ;
}

