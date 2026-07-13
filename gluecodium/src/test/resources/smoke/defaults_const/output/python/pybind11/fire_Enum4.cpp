

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "fire/Enum4.h"

void register_Enum4(py::module_& module) {
    py::enum_<Enum4>(module, "Enum4")
        .value("ENABLED", Enum4::ENABLED)
        .value("DISABLED", Enum4::DISABLED)
        ;
}

