

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/StructWithKotlinPositionalDefaults.h"
#include "cstdint"
#include "string"

void register_StructWithKotlinPositionalDefaults(py::module_& module) {
    py::class_<StructWithKotlinPositionalDefaults>(module, "StructWithKotlinPositionalDefaults")
        .def_readwrite("first_init_field", &StructWithKotlinPositionalDefaults::first_init_field)
        .def_readwrite("first_free_field", &StructWithKotlinPositionalDefaults::first_free_field)
        .def_readwrite("second_init_field", &StructWithKotlinPositionalDefaults::second_init_field)
        .def_readwrite("second_free_field", &StructWithKotlinPositionalDefaults::second_free_field)
        .def_readwrite("third_init_field", &StructWithKotlinPositionalDefaults::third_init_field)
        ;
}

