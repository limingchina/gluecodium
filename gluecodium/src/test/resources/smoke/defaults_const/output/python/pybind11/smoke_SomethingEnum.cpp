

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SomethingEnum.h"

void register_SomethingEnum(py::module_& module) {
    py::enum_<SomethingEnum>(module, "SomethingEnum")
        .value("REALLY_FIRST", SomethingEnum::REALLY_FIRST)
        .value("EXPLICIT", SomethingEnum::EXPLICIT)
        .value("LAST", SomethingEnum::LAST)
        ;
}

