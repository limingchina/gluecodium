

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ScalarKeyframe.h"
#include "cstdint"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ScalarKeyframe = ::gluecodium::smoke::ScalarKeyframe;

void register_ScalarKeyframe(py::module_& module) {
    py::class_<ScalarKeyframe>(module, "ScalarKeyframe")
        .def_readwrite("value", &ScalarKeyframe::value)
        .def_readwrite("offset_in_ms", &ScalarKeyframe::offset_in_ms)
        .def(py::init<double, int32_t>(), py::arg("value"), py::arg("offset_in_ms"))
        ;
}

