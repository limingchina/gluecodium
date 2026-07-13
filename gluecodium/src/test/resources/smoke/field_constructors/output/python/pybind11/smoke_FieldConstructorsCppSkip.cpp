

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldConstructorsCppSkip.h"
#include "cstdint"
#include "string"

void register_FieldConstructorsCppSkip(py::module_& module) {
    py::class_<FieldConstructorsCppSkip>(module, "FieldConstructorsCppSkip")
        .def_readwrite("string_field", &FieldConstructorsCppSkip::string_field)
        .def_readwrite("int_field", &FieldConstructorsCppSkip::int_field)
        ;
}

