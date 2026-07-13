

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldConstructorsNullableTypes.h"
#include "optional"

void register_FieldConstructorsNullableTypes(py::module_& module) {
    py::class_<FieldConstructorsNullableTypes>(module, "FieldConstructorsNullableTypes")
        .def_readwrite("nullable_field", &FieldConstructorsNullableTypes::nullable_field)
        ;
}

