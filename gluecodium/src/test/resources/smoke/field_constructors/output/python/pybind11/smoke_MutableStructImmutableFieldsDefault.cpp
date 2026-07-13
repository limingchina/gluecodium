

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ImmutableDefaultCtor.h"
#include "smoke/MutableStructImmutableFieldsDefault.h"
#include "cstdint"

void register_MutableStructImmutableFieldsDefault(py::module_& module) {
    py::class_<MutableStructImmutableFieldsDefault>(module, "MutableStructImmutableFieldsDefault")
        .def_readwrite("struct_field", &MutableStructImmutableFieldsDefault::struct_field)
        .def_readwrite("int_field", &MutableStructImmutableFieldsDefault::int_field)
        .def_readwrite("bool_field", &MutableStructImmutableFieldsDefault::bool_field)
        ;
}

