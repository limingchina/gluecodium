

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
#include "gluecodium/Optional.h"
#include "smoke/FieldConstructorsNullableTypes.h"

using FieldConstructorsNullableTypes = ::smoke::FieldConstructorsNullableTypes;
using StructWithParameters = ::smoke::FieldConstructorsNullableTypes::StructWithParameters;
using FoodType = ::smoke::FieldConstructorsNullableTypes::FoodType;



void register_smoke_FieldConstructorsNullableTypes(py::module_& module) {
auto cls_FieldConstructorsNullableTypes = py::class_<FieldConstructorsNullableTypes>(module, "smoke_FieldConstructorsNullableTypes")
        .def_property("nullable_field", [](const FieldConstructorsNullableTypes& self) -> decltype(auto) {
            return
                (self.nullable_field)
            ;
        }, [](FieldConstructorsNullableTypes& self, const ::gluecodium::optional< ::smoke::FieldConstructorsNullableTypes::StructWithParameters >& value) {

                self.nullable_field = value;

        })
        .def(py::init<>())
        .def(py::init<::gluecodium::optional< ::smoke::FieldConstructorsNullableTypes::StructWithParameters >>(), py::arg("nullable_field"))
        ;

auto cls_FieldConstructorsNullableTypesStructWithParameters = py::class_<StructWithParameters>(cls_FieldConstructorsNullableTypes, "StructWithParameters")
        .def_property("food_type", [](const StructWithParameters& self) -> decltype(auto) {
            return
                (self.food_type)
            ;
        }, [](StructWithParameters& self, const ::smoke::FieldConstructorsNullableTypes::FoodType value) {

                self.food_type = value;

        })
        .def(py::init<>())
        .def(py::init<::smoke::FieldConstructorsNullableTypes::FoodType>(), py::arg("food_type"))
        ;

auto cls_FieldConstructorsNullableTypesFoodType = py::enum_<FoodType>(cls_FieldConstructorsNullableTypes, "FoodType")
        .value("VEGETABLES", FoodType::VEGETABLES)
        .value("FRUITS", FoodType::FRUITS)
        ;


}
