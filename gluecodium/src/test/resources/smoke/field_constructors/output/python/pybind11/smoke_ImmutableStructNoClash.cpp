

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ImmutableStructNoClash.h"
#include "cstdint"
#include "string"

void register_ImmutableStructNoClash(py::module_& module) {
    py::class_<ImmutableStructNoClash>(module, "ImmutableStructNoClash")
        .def_readwrite("string_field", &ImmutableStructNoClash::string_field)
        .def_readwrite("int_field", &ImmutableStructNoClash::int_field)
        .def_readwrite("bool_field", &ImmutableStructNoClash::bool_field)
        ;
}

