

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EnumOptionSet.h"

void register_EnumOptionSet(py::module_& module) {
    py::enum_<EnumOptionSet>(module, "EnumOptionSet")
        .value("ONE", EnumOptionSet::ONE)
        .value("TWO", EnumOptionSet::TWO)
        .value("THREE", EnumOptionSet::THREE)
        ;
}

