

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SwiftExternalCtor.h"
#include "string"

void register_SwiftExternalCtor(py::module_& module) {
    py::class_<SwiftExternalCtor>(module, "SwiftExternalCtor")
        .def_readwrite("field", &SwiftExternalCtor::field)
        .def("make", &SwiftExternalCtor::make, py::arg("field"))
        ;
}

