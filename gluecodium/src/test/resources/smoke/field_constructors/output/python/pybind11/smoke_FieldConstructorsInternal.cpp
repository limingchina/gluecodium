

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldConstructorsInternal.h"
#include "string"

void register_FieldConstructorsInternal(py::module_& module) {
    py::class_<FieldConstructorsInternal>(module, "FieldConstructorsInternal")
        .def_readwrite("public_field", &FieldConstructorsInternal::public_field)
        .def_readwrite("internal_field", &FieldConstructorsInternal::internal_field)
        ;
}

