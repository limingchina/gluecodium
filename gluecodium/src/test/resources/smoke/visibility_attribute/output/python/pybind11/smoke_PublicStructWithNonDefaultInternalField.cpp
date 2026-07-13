

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/PublicStructWithNonDefaultInternalField.h"
#include "cstdint"

void register_PublicStructWithNonDefaultInternalField(py::module_& module) {
    py::class_<PublicStructWithNonDefaultInternalField>(module, "PublicStructWithNonDefaultInternalField")
        .def_readwrite("defaulted_field", &PublicStructWithNonDefaultInternalField::defaulted_field)
        .def_readwrite("internal_field", &PublicStructWithNonDefaultInternalField::internal_field)
        .def_readwrite("public_field", &PublicStructWithNonDefaultInternalField::public_field)
        ;
}

