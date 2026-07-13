

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/EnumWithAliasWithDeprecated.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EnumWithAliasWithDeprecated = ::gluecodium::smoke::EnumWithAliasWithDeprecated;

void register_EnumWithAliasWithDeprecated(py::module_& module) {
    py::enum_<EnumWithAliasWithDeprecated>(module, "EnumWithAliasWithDeprecated")
        .value("ONE", EnumWithAliasWithDeprecated::ONE)
        .value("TWO", EnumWithAliasWithDeprecated::TWO)
        .value("THREE", EnumWithAliasWithDeprecated::THREE)
        .value("FIRST", EnumWithAliasWithDeprecated::FIRST)
        ;
}

