

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "fire/Enum1.h"

void register_Enum1(py::module_& module) {
    py::enum_<Enum1>(module, "Enum1")
        .value("ENABLED", Enum1::ENABLED)
        .value("DISABLED", Enum1::DISABLED)
        ;
}

