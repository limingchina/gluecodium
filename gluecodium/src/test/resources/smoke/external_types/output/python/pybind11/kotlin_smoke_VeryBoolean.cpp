

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "kotlin_smoke/VeryBoolean.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using VeryBoolean = ::kotlin_smoke::VeryBoolean;

void register_VeryBoolean(py::module_& module) {
    py::class_<VeryBoolean>(module, "VeryBoolean")
        .def_readwrite("value", &VeryBoolean::value)
        .def(py::init<bool>(), py::arg("value"))
        .def("make", &VeryBoolean::make, py::arg("value"))
        ;
}

