

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/PseudoColor.h"

void register_PseudoColor(py::module_& module) {
    py::class_<PseudoColor>(module, "PseudoColor")
        .def_readwrite("red", &PseudoColor::red)
        .def_readwrite("green", &PseudoColor::green)
        .def_readwrite("blue", &PseudoColor::blue)
        .def_readwrite("alpha", &PseudoColor::alpha)
        ;
}

