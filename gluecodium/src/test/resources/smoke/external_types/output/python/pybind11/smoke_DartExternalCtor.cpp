

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartExternalCtor.h"
#include "string"

void register_DartExternalCtor(py::module_& module) {
    py::class_<DartExternalCtor>(module, "DartExternalCtor")
        .def_readwrite("field", &DartExternalCtor::field)
        .def("make", &DartExternalCtor::make, py::arg("field"))
        ;
}

