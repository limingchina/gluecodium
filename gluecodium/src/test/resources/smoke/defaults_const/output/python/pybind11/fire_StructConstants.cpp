

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "fire/StructConstants.h"

void register_StructConstants(py::module_& module) {
    py::class_<StructConstants>(module, "StructConstants")
        ;
}

