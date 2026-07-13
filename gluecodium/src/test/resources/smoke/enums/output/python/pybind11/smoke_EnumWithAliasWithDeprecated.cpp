

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EnumWithAliasWithDeprecated.h"

void register_EnumWithAliasWithDeprecated(py::module_& module) {
    py::enum_<EnumWithAliasWithDeprecated>(module, "EnumWithAliasWithDeprecated")
        .value("ONE", EnumWithAliasWithDeprecated::ONE)
        .value("TWO", EnumWithAliasWithDeprecated::TWO)
        .value("THREE", EnumWithAliasWithDeprecated::THREE)
        .value("FIRST", EnumWithAliasWithDeprecated::FIRST)
        ;
}

