

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/TimePointHash.h"
#include "smoke/DateInterval.h"
#include "chrono"

void register_DateInterval(py::module_& module) {
    py::class_<DateInterval>(module, "DateInterval")
        .def_readwrite("start", &DateInterval::start)
        .def_readwrite("end", &DateInterval::end)
        ;
}

