

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EnumWithAlias.h"

void register_EnumWithAlias(py::module_& module) {
    py::enum_<EnumWithAlias>(module, "EnumWithAlias")
        .value("ONE", EnumWithAlias::ONE)
        .value("TWO", EnumWithAlias::TWO)
        .value("THREE", EnumWithAlias::THREE)
        .value("FIRST", EnumWithAlias::FIRST)
        .value("THE_BEST", EnumWithAlias::THE_BEST)
        ;
}

