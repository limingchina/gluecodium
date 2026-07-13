

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EnumStartsWithOne.h"

void register_EnumStartsWithOne(py::module_& module) {
    py::enum_<EnumStartsWithOne>(module, "EnumStartsWithOne")
        .value("FIRST", EnumStartsWithOne::FIRST)
        .value("SECOND", EnumStartsWithOne::SECOND)
        ;
}

