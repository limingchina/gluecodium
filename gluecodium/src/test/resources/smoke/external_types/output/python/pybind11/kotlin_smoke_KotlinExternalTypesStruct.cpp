

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "kotlin_smoke/Currency.h"
#include "kotlin_smoke/KotlinExternalTypesStruct.h"
#include "kotlin_smoke/Month.h"
#include "kotlin_smoke/Season.h"
#include "kotlin_smoke/SystemColor.h"
#include "kotlin_smoke/TimeZone.h"

void register_KotlinExternalTypesStruct(py::module_& module) {
    py::class_<KotlinExternalTypesStruct>(module, "KotlinExternalTypesStruct")
        .def_readwrite("currency", &KotlinExternalTypesStruct::currency)
        .def_readwrite("time_zone", &KotlinExternalTypesStruct::time_zone)
        .def_readwrite("month", &KotlinExternalTypesStruct::month)
        .def_readwrite("color", &KotlinExternalTypesStruct::color)
        .def_readwrite("season", &KotlinExternalTypesStruct::season)
        ;
}

