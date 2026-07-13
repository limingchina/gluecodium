

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/MutableStructNoClash.h"
#include "cstdint"
#include "string"

void register_MutableStructNoClash(py::module_& module) {
    py::class_<MutableStructNoClash>(module, "MutableStructNoClash")
        .def_readwrite("string_field", &MutableStructNoClash::string_field)
        .def_readwrite("int_field", &MutableStructNoClash::int_field)
        .def_readwrite("bool_field", &MutableStructNoClash::bool_field)
        ;
}

