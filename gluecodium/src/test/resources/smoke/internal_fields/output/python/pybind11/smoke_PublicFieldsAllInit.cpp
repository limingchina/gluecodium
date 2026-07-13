

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/PublicFieldsAllInit.h"
#include "string"

void register_PublicFieldsAllInit(py::module_& module) {
    py::class_<PublicFieldsAllInit>(module, "PublicFieldsAllInit")
        .def_readwrite("public_field", &PublicFieldsAllInit::public_field)
        .def_readwrite("internal_field", &PublicFieldsAllInit::internal_field)
        ;
}

