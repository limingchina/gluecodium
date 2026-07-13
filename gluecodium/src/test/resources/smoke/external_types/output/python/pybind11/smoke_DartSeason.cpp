

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartSeason.h"

void register_DartSeason(py::module_& module) {
    py::enum_<DartSeason>(module, "DartSeason")
        .value("WINTER", DartSeason::WINTER)
        .value("SPRING", DartSeason::SPRING)
        .value("SUMMER", DartSeason::SUMMER)
        .value("AUTUMN", DartSeason::AUTUMN)
        ;
}

