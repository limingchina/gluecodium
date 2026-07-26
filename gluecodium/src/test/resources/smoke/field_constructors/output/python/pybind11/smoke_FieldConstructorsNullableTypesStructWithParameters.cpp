

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FieldConstructorsNullableTypes.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructWithParameters = ::smoke::FieldConstructorsNullableTypes::StructWithParameters;

void register_smoke_FieldConstructorsNullableTypesStructWithParameters(py::module_& module) {
    py::class_<StructWithParameters>(module, "smoke_FieldConstructorsNullableTypesStructWithParameters")
        .def_readwrite("food_type", &StructWithParameters::food_type)
        .def(py::init<>())
        .def(py::init<::smoke::FieldConstructorsNullableTypes::FoodType>(), py::arg("food_type"))
        ;
}

