

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkipOverloadsInDart.h"
#include "memory"
#include "string"

void register_SkipOverloadsInDart(py::module_& module) {
    py::class_<SkipOverloadsInDart>(module, "SkipOverloadsInDart")
        .def("make", &SkipOverloadsInDart::make)
        .def("make", &SkipOverloadsInDart::make, py::arg("input"))
        ;
}

