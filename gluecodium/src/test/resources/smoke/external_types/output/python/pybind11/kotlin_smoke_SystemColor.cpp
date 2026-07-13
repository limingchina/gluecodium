

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "kotlin_smoke/SystemColor.h"

void register_SystemColor(py::module_& module) {
    py::class_<SystemColor>(module, "SystemColor")
        .def_readwrite("red", &SystemColor::red)
        .def_readwrite("green", &SystemColor::green)
        .def_readwrite("blue", &SystemColor::blue)
        .def_readwrite("alpha", &SystemColor::alpha)
        ;
}

