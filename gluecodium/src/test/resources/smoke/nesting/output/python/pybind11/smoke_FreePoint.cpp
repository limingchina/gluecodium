

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FreePoint.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FreePoint = ::smoke::FreePoint;

void register_FreePoint(py::module_& module) {
    py::class_<FreePoint>(module, "FreePoint")
        .def_readwrite("x", &FreePoint::x)
        .def_readwrite("y", &FreePoint::y)
        .def(py::init<>())
        .def(py::init<double, double>(), py::arg("x"), py::arg("y"))
        .def("flip", &FreePoint::flip)

        ;
}

