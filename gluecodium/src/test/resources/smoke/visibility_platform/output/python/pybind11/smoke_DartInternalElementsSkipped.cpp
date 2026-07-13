

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartInternalElementsSkipped.h"
#include "string"

void register_DartInternalElementsSkipped(py::module_& module) {
    py::class_<DartInternalElementsSkipped>(module, "DartInternalElementsSkipped")
        .def_readwrite("bool_field", &DartInternalElementsSkipped::bool_field)
        .def_readwrite("string_field", &DartInternalElementsSkipped::string_field)
        .def("foo", &DartInternalElementsSkipped::foo)
        ;
}

