

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldConstructorWithExcluded.h"
#include "string"

void register_FieldConstructorWithExcluded(py::module_& module) {
    py::class_<FieldConstructorWithExcluded>(module, "FieldConstructorWithExcluded")
        .def_readwrite("string_field", &FieldConstructorWithExcluded::string_field)
        ;
}

