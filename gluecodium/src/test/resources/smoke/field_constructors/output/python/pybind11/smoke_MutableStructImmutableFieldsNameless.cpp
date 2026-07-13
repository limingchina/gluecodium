

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ImmutableNamelessCtor.h"
#include "smoke/MutableStructImmutableFieldsNameless.h"
#include "cstdint"

void register_MutableStructImmutableFieldsNameless(py::module_& module) {
    py::class_<MutableStructImmutableFieldsNameless>(module, "MutableStructImmutableFieldsNameless")
        .def_readwrite("struct_field", &MutableStructImmutableFieldsNameless::struct_field)
        .def_readwrite("int_field", &MutableStructImmutableFieldsNameless::int_field)
        .def_readwrite("bool_field", &MutableStructImmutableFieldsNameless::bool_field)
        ;
}

