

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartDeprecatedPosDefaults.h"
#include "cstdint"
#include "string"

void register_DartDeprecatedPosDefaults(py::module_& module) {
    py::class_<DartDeprecatedPosDefaults>(module, "DartDeprecatedPosDefaults")
        .def_readwrite("int_field", &DartDeprecatedPosDefaults::int_field)
        .def_readwrite("string_field", &DartDeprecatedPosDefaults::string_field)
        ;
}

