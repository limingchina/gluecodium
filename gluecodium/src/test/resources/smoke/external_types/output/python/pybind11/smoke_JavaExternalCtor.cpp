

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/JavaExternalCtor.h"
#include "string"

void register_JavaExternalCtor(py::module_& module) {
    py::class_<JavaExternalCtor>(module, "JavaExternalCtor")
        .def_readwrite("field", &JavaExternalCtor::field)
        .def("make", &JavaExternalCtor::make, py::arg("field"))
        ;
}

