

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/EnumWithToStringHelper.h"
#include "string_view"

using EnumWithToStringHelper = ::smoke::EnumWithToStringHelper;



void register_smoke_EnumWithToStringHelper(py::module_& module) {
auto cls_EnumWithToStringHelper = py::enum_<EnumWithToStringHelper>(module, "smoke_EnumWithToStringHelper")
        .value("FIRST", EnumWithToStringHelper::FIRST)
        .value("SECOND", EnumWithToStringHelper::SECOND)
        ;


}
