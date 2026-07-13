

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ImmutableStructWithClash.h"
#include "cstdint"
#include "string"

void register_ImmutableStructWithClash(py::module_& module) {
    py::class_<ImmutableStructWithClash>(module, "ImmutableStructWithClash")
        .def_readwrite("string_field", &ImmutableStructWithClash::string_field)
        .def_readwrite("int_field", &ImmutableStructWithClash::int_field)
        .def_readwrite("bool_field", &ImmutableStructWithClash::bool_field)
        ;
}

