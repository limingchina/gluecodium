

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FieldConstructorsNullableTypes.h"
#include "optional"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FieldConstructorsNullableTypes = ::smoke::FieldConstructorsNullableTypes;

void register_FieldConstructorsNullableTypes(py::module_& module) {
    py::class_<FieldConstructorsNullableTypes>(module, "FieldConstructorsNullableTypes")
        .def_readwrite("nullable_field", &FieldConstructorsNullableTypes::nullable_field)
        .def(py::init<>())
        ;
}

