

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/TimePointHash.h"
#include "smoke/DateDefaults.h"
#include "chrono"

void register_DateDefaults(py::module_& module) {
    py::class_<DateDefaults>(module, "DateDefaults")
        .def_readwrite("date_time", &DateDefaults::date_time)
        .def_readwrite("date_time_utc", &DateDefaults::date_time_utc)
        .def_readwrite("before_epoch", &DateDefaults::before_epoch)
        .def_readwrite("exactly_epoch", &DateDefaults::exactly_epoch)
        ;
}

