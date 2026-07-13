

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/PublicFieldsAllInitPosDefaults.h"
#include "string"

void register_PublicFieldsAllInitPosDefaults(py::module_& module) {
    py::class_<PublicFieldsAllInitPosDefaults>(module, "PublicFieldsAllInitPosDefaults")
        .def_readwrite("public_field", &PublicFieldsAllInitPosDefaults::public_field)
        .def_readwrite("internal_field", &PublicFieldsAllInitPosDefaults::internal_field)
        ;
}

