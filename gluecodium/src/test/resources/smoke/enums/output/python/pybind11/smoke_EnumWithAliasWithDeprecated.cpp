

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/EnumWithAliasWithDeprecated.h"

using EnumWithAliasWithDeprecated = ::smoke::EnumWithAliasWithDeprecated;



void register_smoke_EnumWithAliasWithDeprecated(py::module_& module) {
auto cls_EnumWithAliasWithDeprecated = py::enum_<EnumWithAliasWithDeprecated>(module, "smoke_EnumWithAliasWithDeprecated")
        .value("ONE", EnumWithAliasWithDeprecated::ONE)
        .value("TWO", EnumWithAliasWithDeprecated::TWO)
        .value("THREE", EnumWithAliasWithDeprecated::THREE)
        .value("FIRST", EnumWithAliasWithDeprecated::FIRST)
        ;


}
