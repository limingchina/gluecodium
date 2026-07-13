

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkippedOverloads.h"
#include "memory"
#include "string"

void register_SkippedOverloads(py::module_& module) {
    py::class_<SkippedOverloads>(module, "SkippedOverloads")
        .def("make", &SkippedOverloads::make)
        .def("make_for_dart", &SkippedOverloads::make_for_dart, py::arg("input"))
        ;
}

