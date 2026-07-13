

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EquatableStructWithInternalFields.h"
#include "string"

void register_EquatableStructWithInternalFields(py::module_& module) {
    py::class_<EquatableStructWithInternalFields>(module, "EquatableStructWithInternalFields")
        .def_readwrite("public_field", &EquatableStructWithInternalFields::public_field)
        .def_readwrite("internal_field", &EquatableStructWithInternalFields::internal_field)
        .def_readwrite("internal_list_field", &EquatableStructWithInternalFields::internal_list_field)
        .def_readwrite("internal_map_field", &EquatableStructWithInternalFields::internal_map_field)
        .def_readwrite("internal_set_field", &EquatableStructWithInternalFields::internal_set_field)
        ;
}

