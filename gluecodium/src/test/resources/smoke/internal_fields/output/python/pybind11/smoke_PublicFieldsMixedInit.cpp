

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/PublicFieldsMixedInit.h"
#include "string"

void register_PublicFieldsMixedInit(py::module_& module) {
    py::class_<PublicFieldsMixedInit>(module, "PublicFieldsMixedInit")
        .def_readwrite("public_field1", &PublicFieldsMixedInit::public_field1)
        .def_readwrite("public_field2", &PublicFieldsMixedInit::public_field2)
        .def_readwrite("internal_field", &PublicFieldsMixedInit::internal_field)
        ;
}

