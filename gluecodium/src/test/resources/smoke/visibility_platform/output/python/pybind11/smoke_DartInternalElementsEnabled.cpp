

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartInternalElementsEnabled.h"
#include "string"

void register_DartInternalElementsEnabled(py::module_& module) {
    py::class_<DartInternalElementsEnabled>(module, "DartInternalElementsEnabled")
        .def_readwrite("bool_field", &DartInternalElementsEnabled::bool_field)
        .def_readwrite("string_field", &DartInternalElementsEnabled::string_field)
        .def("foo", &DartInternalElementsEnabled::foo)
        ;
}

