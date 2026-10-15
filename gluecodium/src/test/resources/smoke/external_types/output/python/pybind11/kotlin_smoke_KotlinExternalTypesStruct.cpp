

#include <Python.h>
#include <pybind11/pybind11.h>
#include "_opaque_types.h"
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "kotlin_smoke/Currency.h"
#include "kotlin_smoke/KotlinExternalTypesStruct.h"
#include "kotlin_smoke/Month.h"
#include "kotlin_smoke/Season.h"
#include "kotlin_smoke/SystemColor.h"
#include "kotlin_smoke/TimeZone.h"

using KotlinExternalTypesStruct = ::kotlin_smoke::KotlinExternalTypesStruct;



void register_kotlin_smoke_KotlinExternalTypesStruct(py::module_& module) {
auto cls_KotlinExternalTypesStruct = py::class_<KotlinExternalTypesStruct>(module, "kotlin_smoke_KotlinExternalTypesStruct")
        .def_property_readonly("currency", [](const KotlinExternalTypesStruct& self) -> decltype(auto) {
            return
                (self.currency)
            ;
        })
        .def_property("time_zone", [](const KotlinExternalTypesStruct& self) -> decltype(auto) {
            return
                (self.time_zone)
            ;
        }, [](KotlinExternalTypesStruct& self, const ::kotlin_smoke::TimeZone& value) {

                self.time_zone = value;

        })
        .def_property("month", [](const KotlinExternalTypesStruct& self) -> decltype(auto) {
            return
                (self.month)
            ;
        }, [](KotlinExternalTypesStruct& self, const ::kotlin_smoke::Month value) {

                self.month = value;

        })
        .def_property("color", [](const KotlinExternalTypesStruct& self) -> decltype(auto) {
            return
                (self.color)
            ;
        }, [](KotlinExternalTypesStruct& self, const ::kotlin_smoke::SystemColor& value) {

                self.color = value;

        })
        .def_property("season", [](const KotlinExternalTypesStruct& self) -> decltype(auto) {
            return
                (self.season)
            ;
        }, [](KotlinExternalTypesStruct& self, const ::kotlin_smoke::Season value) {

                self.season = value;

        })
        .def(py::init<::kotlin_smoke::Currency, ::kotlin_smoke::TimeZone, ::kotlin_smoke::Month, ::kotlin_smoke::SystemColor, ::kotlin_smoke::Season>(), py::arg("currency"), py::arg("time_zone"), py::arg("month"), py::arg("color"), py::arg("season"))
        ;


}
