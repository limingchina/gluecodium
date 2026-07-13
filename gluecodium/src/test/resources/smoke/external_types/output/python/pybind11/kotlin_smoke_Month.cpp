

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "kotlin_smoke/Month.h"

void register_Month(py::module_& module) {
    py::enum_<Month>(module, "Month")
        .value("JANUARY", Month::JANUARY)
        .value("FEBRUARY", Month::FEBRUARY)
        .value("MARCH", Month::MARCH)
        ;
}

