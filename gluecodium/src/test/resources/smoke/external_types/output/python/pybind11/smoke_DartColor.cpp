

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/DartColor.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DartColor = ::gluecodium::smoke::DartColor;

void register_DartColor(py::module_& module) {
    py::class_<DartColor>(module, "DartColor")
        .def_readwrite("red", &DartColor::red)
        .def_readwrite("green", &DartColor::green)
        .def_readwrite("blue", &DartColor::blue)
        .def_readwrite("alpha", &DartColor::alpha)
        ;
}

