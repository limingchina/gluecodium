

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FreePoint.h"

void register_FreePoint(py::module_& module) {
    py::class_<FreePoint>(module, "FreePoint")
        .def_readwrite("x", &FreePoint::x)
        .def_readwrite("y", &FreePoint::y)
        .def("flip", &FreePoint::flip)
        ;
}

