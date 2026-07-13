

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/SwiftMethodOverloads.h"
#include "string"
#include "vector"

void register_SwiftMethodOverloads(py::module_& module) {
    py::class_<SwiftMethodOverloads>(module, "SwiftMethodOverloads")
        .def("one", &SwiftMethodOverloads::one, py::arg("input"))
        .def("two", &SwiftMethodOverloads::two, py::arg("input"))
        ;
}

