

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/TimePointHash.h"
#include "smoke/DateDefaults.h"
#include "chrono"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DateDefaults = ::gluecodium::smoke::DateDefaults;

void register_DateDefaults(py::module_& module) {
    py::class_<DateDefaults>(module, "DateDefaults")
        .def_readwrite("date_time", &DateDefaults::date_time)
        .def_readwrite("date_time_utc", &DateDefaults::date_time_utc)
        .def_readwrite("before_epoch", &DateDefaults::before_epoch)
        .def_readwrite("exactly_epoch", &DateDefaults::exactly_epoch)
        ;
}

