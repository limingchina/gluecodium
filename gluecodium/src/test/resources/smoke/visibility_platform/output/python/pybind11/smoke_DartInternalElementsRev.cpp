

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartInternalElementsRev.h"
#include "string"

void register_DartInternalElementsRev(py::module_& module) {
    py::class_<DartInternalElementsRev>(module, "DartInternalElementsRev")
        .def_readwrite("string_field", &DartInternalElementsRev::string_field)
        .def("foo", &DartInternalElementsRev::foo)
        ;
}

