

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldConstructorsParameterDefaults.h"
#include "cstdint"
#include "string"

void register_FieldConstructorsParameterDefaults(py::module_& module) {
    py::class_<FieldConstructorsParameterDefaults>(module, "FieldConstructorsParameterDefaults")
        .def_readwrite("string_field", &FieldConstructorsParameterDefaults::string_field)
        .def_readwrite("int_field", &FieldConstructorsParameterDefaults::int_field)
        .def_readwrite("bool_field", &FieldConstructorsParameterDefaults::bool_field)
        ;
}

