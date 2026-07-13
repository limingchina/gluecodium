

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkipFieldInPlatform.h"
#include "cstdint"
#include "string"

void register_SkipFieldInPlatform(py::module_& module) {
    py::class_<SkipFieldInPlatform>(module, "SkipFieldInPlatform")
        .def_readwrite("int_field", &SkipFieldInPlatform::int_field)
        .def_readwrite("string_field", &SkipFieldInPlatform::string_field)
        .def_readwrite("bool_field", &SkipFieldInPlatform::bool_field)
        ;
}

