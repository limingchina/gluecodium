

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DateAlias.h"
#include "smoke/DateDefaultsAliased.h"

void register_DateDefaultsAliased(py::module_& module) {
    py::class_<DateDefaultsAliased>(module, "DateDefaultsAliased")
        .def_readwrite("date_time", &DateDefaultsAliased::date_time)
        .def_readwrite("date_time_utc", &DateDefaultsAliased::date_time_utc)
        .def_readwrite("before_epoch", &DateDefaultsAliased::before_epoch)
        .def_readwrite("exactly_epoch", &DateDefaultsAliased::exactly_epoch)
        ;
}

