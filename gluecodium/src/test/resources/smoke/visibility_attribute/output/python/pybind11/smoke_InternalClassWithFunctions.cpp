

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/InternalClassWithFunctions.h"
#include "memory"
#include "string"

void register_InternalClassWithFunctions(py::module_& module) {
    py::class_<InternalClassWithFunctions>(module, "InternalClassWithFunctions")
        .def("foo_bar", &InternalClassWithFunctions::foo_bar)
        .def("make", &InternalClassWithFunctions::make)
        .def("make", &InternalClassWithFunctions::make, py::arg("foo"))
        ;
}

