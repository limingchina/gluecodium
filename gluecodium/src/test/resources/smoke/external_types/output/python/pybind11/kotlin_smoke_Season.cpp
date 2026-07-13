

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "kotlin_smoke/Season.h"

void register_Season(py::module_& module) {
    py::enum_<Season>(module, "Season")
        .value("WINTER", Season::WINTER)
        .value("SPRING", Season::SPRING)
        .value("SUMMER", Season::SUMMER)
        .value("AUTUMN", Season::AUTUMN)
        ;
}

