

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "fire/Enum2.h"

void register_Enum2(py::module_& module) {
    py::enum_<Enum2>(module, "Enum2")
        .value("ENABLED", Enum2::ENABLED)
        .value("DISABLED", Enum2::DISABLED)
        ;
}

