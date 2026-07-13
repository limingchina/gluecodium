

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/DateAlias.h"
#include "smoke/DateDefaultsAliased.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DateDefaultsAliased = ::gluecodium::smoke::DateDefaultsAliased;

void register_DateDefaultsAliased(py::module_& module) {
    py::class_<DateDefaultsAliased>(module, "DateDefaultsAliased")
        .def_readwrite("date_time", &DateDefaultsAliased::date_time)
        .def_readwrite("date_time_utc", &DateDefaultsAliased::date_time_utc)
        .def_readwrite("before_epoch", &DateDefaultsAliased::before_epoch)
        .def_readwrite("exactly_epoch", &DateDefaultsAliased::exactly_epoch)
        .def(py::init<>())
        .def(py::init<::std::chrono::system_clock::time_point, ::std::chrono::system_clock::time_point, ::std::chrono::system_clock::time_point, ::std::chrono::system_clock::time_point>(), py::arg("date_time"), py::arg("date_time_utc"), py::arg("before_epoch"), py::arg("exactly_epoch"))
        ;
}

