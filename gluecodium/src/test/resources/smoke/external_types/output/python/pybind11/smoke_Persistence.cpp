

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/Persistence.h"

void register_Persistence(py::module_& module) {
    py::enum_<Persistence>(module, "Persistence")
        .value("NONE", Persistence::NONE)
        .value("FOR_SESSION", Persistence::FOR_SESSION)
        .value("PERMANENT", Persistence::PERMANENT)
        ;
}

