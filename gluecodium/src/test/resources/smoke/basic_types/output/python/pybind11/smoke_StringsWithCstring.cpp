

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/StringsWithCstring.h"
#include "string"

void register_StringsWithCstring(py::module_& module) {
    py::class_<StringsWithCstring>(module, "StringsWithCstring")
        .def("return_input_string_type", &StringsWithCstring::return_input_string, py::arg("input_string"))
        .def("return_input_string", &StringsWithCstring::return_input_string, py::arg("input_string"))
        ;
}

