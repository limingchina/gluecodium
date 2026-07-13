

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldConstructorsInternalFields.h"
#include "cstdint"
#include "string"

void register_FieldConstructorsInternalFields(py::module_& module) {
    py::class_<FieldConstructorsInternalFields>(module, "FieldConstructorsInternalFields")
        .def_readwrite("string_field", &FieldConstructorsInternalFields::string_field)
        .def_readwrite("int_field", &FieldConstructorsInternalFields::int_field)
        .def_readwrite("bool_field", &FieldConstructorsInternalFields::bool_field)
        ;
}

