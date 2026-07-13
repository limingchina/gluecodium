

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/StructWithSomeDefaults.h"
#include "cstdint"
#include "string"

void register_StructWithSomeDefaults(py::module_& module) {
    py::class_<StructWithSomeDefaults>(module, "StructWithSomeDefaults")
        .def_readwrite("int_field", &StructWithSomeDefaults::int_field)
        .def_readwrite("string_field", &StructWithSomeDefaults::string_field)
        ;
}

