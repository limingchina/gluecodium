

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "kotlin_smoke/VeryBoolean.h"

void register_VeryBoolean(py::module_& module) {
    py::class_<VeryBoolean>(module, "VeryBoolean")
        .def_readwrite("value", &VeryBoolean::value)
        .def("make", &VeryBoolean::make, py::arg("value"))
        ;
}

