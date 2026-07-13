

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/EnumWithAccessibleValues.h"
#include "array"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EnumWithAccessibleValues = ::gluecodium::smoke::EnumWithAccessibleValues;

void register_EnumWithAccessibleValues(py::module_& module) {
    py::enum_<EnumWithAccessibleValues>(module, "EnumWithAccessibleValues")
        .value("FOO", EnumWithAccessibleValues::FOO)
        .value("BAR", EnumWithAccessibleValues::BAR)
        .value("BAZ", EnumWithAccessibleValues::BAZ)
        .value("FOO_ALIAS", EnumWithAccessibleValues::FOO_ALIAS)
        ;
}

