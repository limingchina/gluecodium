

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/PublicFieldsNone.h"

void register_PublicFieldsNone(py::module_& module) {
    py::class_<PublicFieldsNone>(module, "PublicFieldsNone")
        .def_readwrite("internal_field", &PublicFieldsNone::internal_field)
        ;
}

