

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/Currency.h"
#include "smoke/JavaExternalTypesStruct.h"
#include "smoke/Month.h"
#include "smoke/Season.h"
#include "smoke/SystemColor.h"
#include "smoke/TimeZone.h"

void register_JavaExternalTypesStruct(py::module_& module) {
    py::class_<JavaExternalTypesStruct>(module, "JavaExternalTypesStruct")
        .def_readwrite("currency", &JavaExternalTypesStruct::currency)
        .def_readwrite("time_zone", &JavaExternalTypesStruct::time_zone)
        .def_readwrite("month", &JavaExternalTypesStruct::month)
        .def_readwrite("color", &JavaExternalTypesStruct::color)
        .def_readwrite("season", &JavaExternalTypesStruct::season)
        ;
}

