

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartPublicElementsEnabled.h"

void register_DartPublicElementsEnabled(py::module_& module) {
    py::class_<DartPublicElementsEnabled>(module, "DartPublicElementsEnabled")
        .def_readwrite("bool_field", &DartPublicElementsEnabled::bool_field)
        .def_readwrite("string_field", &DartPublicElementsEnabled::string_field)
        .def("foo", &DartPublicElementsEnabled::foo)
        ;
}

