

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
#include "smoke/Currency.h"
#include "smoke/JavaExternalTypesStruct.h"
#include "smoke/Month.h"
#include "smoke/Season.h"
#include "smoke/SystemColor.h"
#include "smoke/TimeZone.h"

using JavaExternalTypesStruct = ::smoke::JavaExternalTypesStruct;



void register_smoke_JavaExternalTypesStruct(py::module_& module) {
auto cls_JavaExternalTypesStruct = py::class_<JavaExternalTypesStruct>(module, "smoke_JavaExternalTypesStruct")
        .def_property_readonly("currency", [](const JavaExternalTypesStruct& self) -> decltype(auto) {
            return
                (self.currency)
            ;
        })
        .def_property("time_zone", [](const JavaExternalTypesStruct& self) -> decltype(auto) {
            return
                (self.time_zone)
            ;
        }, [](JavaExternalTypesStruct& self, const ::smoke::TimeZone& value) {

                self.time_zone = value;

        })
        .def_property("month", [](const JavaExternalTypesStruct& self) -> decltype(auto) {
            return
                (self.month)
            ;
        }, [](JavaExternalTypesStruct& self, const ::smoke::Month value) {

                self.month = value;

        })
        .def_property("color", [](const JavaExternalTypesStruct& self) -> decltype(auto) {
            return
                (self.color)
            ;
        }, [](JavaExternalTypesStruct& self, const ::smoke::SystemColor& value) {

                self.color = value;

        })
        .def_property("season", [](const JavaExternalTypesStruct& self) -> decltype(auto) {
            return
                (self.season)
            ;
        }, [](JavaExternalTypesStruct& self, const ::smoke::Season value) {

                self.season = value;

        })
        .def(py::init<::smoke::Currency, ::smoke::TimeZone, ::smoke::Month, ::smoke::SystemColor, ::smoke::Season>(), py::arg("currency"), py::arg("time_zone"), py::arg("month"), py::arg("color"), py::arg("season"))
        ;


}
