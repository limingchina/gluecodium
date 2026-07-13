

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SwiftConstructorOverloads.h"
#include "memory"
#include "string"

void register_SwiftConstructorOverloads(py::module_& module) {
    py::class_<SwiftConstructorOverloads>(module, "SwiftConstructorOverloads")
        .def("make", &SwiftConstructorOverloads::make, py::arg("input"))
        .def("make_do", &SwiftConstructorOverloads::make_do, py::arg("throughput"))
        ;
}

