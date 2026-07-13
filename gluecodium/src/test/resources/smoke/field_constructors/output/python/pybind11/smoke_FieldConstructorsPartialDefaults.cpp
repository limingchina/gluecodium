

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldConstructorsPartialDefaults.h"
#include "cstdint"
#include "string"

void register_FieldConstructorsPartialDefaults(py::module_& module) {
    py::class_<FieldConstructorsPartialDefaults>(module, "FieldConstructorsPartialDefaults")
        .def_readwrite("string_field", &FieldConstructorsPartialDefaults::string_field)
        .def_readwrite("int_field", &FieldConstructorsPartialDefaults::int_field)
        .def_readwrite("bool_field", &FieldConstructorsPartialDefaults::bool_field)
        ;
}

