

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "fire/Enum3.h"

void register_Enum3(py::module_& module) {
    py::enum_<Enum3>(module, "Enum3")
        .value("ENABLED", Enum3::ENABLED)
        .value("DISABLED", Enum3::DISABLED)
        ;
}

