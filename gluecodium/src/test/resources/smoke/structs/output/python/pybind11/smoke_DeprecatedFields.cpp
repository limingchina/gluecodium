

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DeprecatedFields.h"
#include "string"

void register_DeprecatedFields(py::module_& module) {
    py::class_<DeprecatedFields>(module, "DeprecatedFields")
        .def_readwrite("normal_field1", &DeprecatedFields::normal_field1)
        .def_readwrite("deprecated_field", &DeprecatedFields::deprecated_field)
        .def_readwrite("normal_field2", &DeprecatedFields::normal_field2)
        ;
}

