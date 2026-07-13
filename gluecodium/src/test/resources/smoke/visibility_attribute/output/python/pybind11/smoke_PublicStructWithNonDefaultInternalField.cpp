

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/PublicStructWithNonDefaultInternalField.h"
#include "cstdint"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using PublicStructWithNonDefaultInternalField = ::gluecodium::smoke::PublicStructWithNonDefaultInternalField;

void register_PublicStructWithNonDefaultInternalField(py::module_& module) {
    py::class_<PublicStructWithNonDefaultInternalField>(module, "PublicStructWithNonDefaultInternalField")
        .def_readwrite("defaulted_field", &PublicStructWithNonDefaultInternalField::defaulted_field)
        .def_readwrite("internal_field", &PublicStructWithNonDefaultInternalField::internal_field)
        .def_readwrite("public_field", &PublicStructWithNonDefaultInternalField::public_field)
        .def(py::init<int32_t, ::std::string, bool>(), py::arg("defaulted_field"), py::arg("internal_field"), py::arg("public_field"))
        ;
}

