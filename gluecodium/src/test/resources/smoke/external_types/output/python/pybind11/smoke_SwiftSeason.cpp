

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SwiftSeason.h"

void register_SwiftSeason(py::module_& module) {
    py::enum_<SwiftSeason>(module, "SwiftSeason")
        .value("WINTER", SwiftSeason::WINTER)
        .value("SPRING", SwiftSeason::SPRING)
        .value("SUMMER", SwiftSeason::SUMMER)
        .value("AUTUMN", SwiftSeason::AUTUMN)
        ;
}

