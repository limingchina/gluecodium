

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "kotlin_smoke/TimeZone.h"
#include "cstdint"

void register_TimeZone(py::module_& module) {
    py::class_<TimeZone>(module, "TimeZone")
        .def_readwrite("raw_offset", &TimeZone::raw_offset)
        ;
}

