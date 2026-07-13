

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/AmbiguousConstants.h"

void register_AmbiguousConstants(py::module_& module) {
    py::class_<AmbiguousConstants>(module, "AmbiguousConstants")
        ;
}

