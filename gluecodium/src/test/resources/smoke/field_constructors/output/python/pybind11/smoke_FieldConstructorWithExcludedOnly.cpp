

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldConstructorWithExcludedOnly.h"
#include "string"

void register_FieldConstructorWithExcludedOnly(py::module_& module) {
    py::class_<FieldConstructorWithExcludedOnly>(module, "FieldConstructorWithExcludedOnly")
        .def_readwrite("string_field", &FieldConstructorWithExcludedOnly::string_field)
        ;
}

