

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ScalarKeyframe.h"
#include "cstdint"

void register_ScalarKeyframe(py::module_& module) {
    py::class_<ScalarKeyframe>(module, "ScalarKeyframe")
        .def_readwrite("value", &ScalarKeyframe::value)
        .def_readwrite("offset_in_ms", &ScalarKeyframe::offset_in_ms)
        ;
}

