

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SystemColor.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SystemColor = ::gluecodium::smoke::SystemColor;

void register_SystemColor(py::module_& module) {
    py::class_<SystemColor>(module, "SystemColor")
        .def_readwrite("red", &SystemColor::red)
        .def_readwrite("green", &SystemColor::green)
        .def_readwrite("blue", &SystemColor::blue)
        .def_readwrite("alpha", &SystemColor::alpha)
        .def(py::init<float, float, float, float>(), py::arg("red"), py::arg("green"), py::arg("blue"), py::arg("alpha"))
        ;
}

