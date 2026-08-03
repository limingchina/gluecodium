

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
#include "kotlin_smoke/Currency.h"
#include "kotlin_smoke/KotlinExternalTypesStruct.h"
#include "kotlin_smoke/Month.h"
#include "kotlin_smoke/Season.h"
#include "kotlin_smoke/SystemColor.h"
#include "kotlin_smoke/TimeZone.h"

using KotlinExternalTypesStruct = ::kotlin_smoke::KotlinExternalTypesStruct;



void register_kotlin_smoke_KotlinExternalTypesStruct(py::module_& module) {
auto cls_KotlinExternalTypesStruct = py::class_<KotlinExternalTypesStruct>(module, "kotlin_smoke_KotlinExternalTypesStruct")
        .def_readonly("currency", &KotlinExternalTypesStruct::currency)
        .def_readwrite("time_zone", &KotlinExternalTypesStruct::time_zone)
        .def_readwrite("month", &KotlinExternalTypesStruct::month)
        .def_readwrite("color", &KotlinExternalTypesStruct::color)
        .def_readwrite("season", &KotlinExternalTypesStruct::season)
        .def(py::init<::kotlin_smoke::Currency, ::kotlin_smoke::TimeZone, ::kotlin_smoke::Month, ::kotlin_smoke::SystemColor, ::kotlin_smoke::Season>(), py::arg("currency"), py::arg("time_zone"), py::arg("month"), py::arg("color"), py::arg("season"))
        ;


}
