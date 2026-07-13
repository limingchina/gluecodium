

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ImmutableStructNoClash.h"
#include "smoke/MutableStructImmutableFields.h"
#include "cstdint"

void register_MutableStructImmutableFields(py::module_& module) {
    py::class_<MutableStructImmutableFields>(module, "MutableStructImmutableFields")
        .def_readwrite("struct_field", &MutableStructImmutableFields::struct_field)
        .def_readwrite("int_field", &MutableStructImmutableFields::int_field)
        .def_readwrite("bool_field", &MutableStructImmutableFields::bool_field)
        ;
}

