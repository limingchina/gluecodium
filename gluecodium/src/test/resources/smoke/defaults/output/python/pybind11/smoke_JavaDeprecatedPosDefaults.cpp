

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/JavaDeprecatedPosDefaults.h"
#include "cstdint"
#include "string"

void register_JavaDeprecatedPosDefaults(py::module_& module) {
    py::class_<JavaDeprecatedPosDefaults>(module, "JavaDeprecatedPosDefaults")
        .def_readwrite("first_init_field", &JavaDeprecatedPosDefaults::first_init_field)
        .def_readwrite("first_free_field", &JavaDeprecatedPosDefaults::first_free_field)
        ;
}

