

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/StructWithAllDefaults.h"
#include "cstdint"
#include "string"

void register_StructWithAllDefaults(py::module_& module) {
    py::class_<StructWithAllDefaults>(module, "StructWithAllDefaults")
        .def_readwrite("int_field", &StructWithAllDefaults::int_field)
        .def_readwrite("string_field", &StructWithAllDefaults::string_field)
        ;
}

