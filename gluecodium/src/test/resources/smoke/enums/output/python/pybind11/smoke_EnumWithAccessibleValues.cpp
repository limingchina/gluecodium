

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EnumWithAccessibleValues.h"
#include "array"

void register_EnumWithAccessibleValues(py::module_& module) {
    py::enum_<EnumWithAccessibleValues>(module, "EnumWithAccessibleValues")
        .value("FOO", EnumWithAccessibleValues::FOO)
        .value("BAR", EnumWithAccessibleValues::BAR)
        .value("BAZ", EnumWithAccessibleValues::BAZ)
        .value("FOO_ALIAS", EnumWithAccessibleValues::FOO_ALIAS)
        ;
}

