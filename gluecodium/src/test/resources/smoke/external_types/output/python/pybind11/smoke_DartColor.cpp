

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartColor.h"

void register_DartColor(py::module_& module) {
    py::class_<DartColor>(module, "DartColor")
        .def_readwrite("red", &DartColor::red)
        .def_readwrite("green", &DartColor::green)
        .def_readwrite("blue", &DartColor::blue)
        .def_readwrite("alpha", &DartColor::alpha)
        ;
}

