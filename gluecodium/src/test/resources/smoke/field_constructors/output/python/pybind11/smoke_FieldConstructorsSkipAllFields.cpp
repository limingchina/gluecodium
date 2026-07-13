

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldConstructorsSkipAllFields.h"
#include "cstdint"
#include "string"

void register_FieldConstructorsSkipAllFields(py::module_& module) {
    py::class_<FieldConstructorsSkipAllFields>(module, "FieldConstructorsSkipAllFields")
        .def_readwrite("string_field", &FieldConstructorsSkipAllFields::string_field)
        .def_readwrite("int_field", &FieldConstructorsSkipAllFields::int_field)
        ;
}

