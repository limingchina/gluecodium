

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/StructWithJavaPositionalDefaults.h"
#include "cstdint"
#include "string"

void register_StructWithJavaPositionalDefaults(py::module_& module) {
    py::class_<StructWithJavaPositionalDefaults>(module, "StructWithJavaPositionalDefaults")
        .def_readwrite("first_init_field", &StructWithJavaPositionalDefaults::first_init_field)
        .def_readwrite("first_free_field", &StructWithJavaPositionalDefaults::first_free_field)
        .def_readwrite("second_init_field", &StructWithJavaPositionalDefaults::second_init_field)
        .def_readwrite("second_free_field", &StructWithJavaPositionalDefaults::second_free_field)
        .def_readwrite("third_init_field", &StructWithJavaPositionalDefaults::third_init_field)
        ;
}

