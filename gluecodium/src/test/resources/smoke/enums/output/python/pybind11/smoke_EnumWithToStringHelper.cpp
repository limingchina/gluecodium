

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EnumWithToStringHelper.h"
#include "string_view"

void register_EnumWithToStringHelper(py::module_& module) {
    py::enum_<EnumWithToStringHelper>(module, "EnumWithToStringHelper")
        .value("FIRST", EnumWithToStringHelper::FIRST)
        .value("SECOND", EnumWithToStringHelper::SECOND)
        ;
}

