

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/PublicFieldsNoInit.h"
#include "string"

void register_PublicFieldsNoInit(py::module_& module) {
    py::class_<PublicFieldsNoInit>(module, "PublicFieldsNoInit")
        .def_readwrite("public_field", &PublicFieldsNoInit::public_field)
        .def_readwrite("internal_field", &PublicFieldsNoInit::internal_field)
        ;
}

