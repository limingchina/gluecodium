

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FieldConstructorsNullableTypes.h"
#include "optional"

using FieldConstructorsNullableTypes = ::smoke::FieldConstructorsNullableTypes;
using StructWithParameters = ::smoke::FieldConstructorsNullableTypes::StructWithParameters;
using FoodType = ::smoke::FieldConstructorsNullableTypes::FoodType;



void register_smoke_FieldConstructorsNullableTypes(py::module_& module) {
auto cls_FieldConstructorsNullableTypes = py::class_<FieldConstructorsNullableTypes>(module, "smoke_FieldConstructorsNullableTypes")
        .def_readwrite("nullable_field", &FieldConstructorsNullableTypes::nullable_field)
        .def(py::init<>())
        .def(py::init<std::optional< ::smoke::FieldConstructorsNullableTypes::StructWithParameters >>(), py::arg("nullable_field"))
        ;

auto cls_FieldConstructorsNullableTypesStructWithParameters = py::class_<StructWithParameters>(cls_FieldConstructorsNullableTypes, "StructWithParameters")
        .def_readwrite("food_type", &StructWithParameters::food_type)
        .def(py::init<>())
        .def(py::init<::smoke::FieldConstructorsNullableTypes::FoodType>(), py::arg("food_type"))
        ;

auto cls_FieldConstructorsNullableTypesFoodType = py::enum_<FoodType>(cls_FieldConstructorsNullableTypes, "FoodType")
        .value("VEGETABLES", FoodType::VEGETABLES)
        .value("FRUITS", FoodType::FRUITS)
        ;


}
