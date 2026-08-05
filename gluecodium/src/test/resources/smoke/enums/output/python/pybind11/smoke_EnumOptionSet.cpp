

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
#include "smoke/EnumOptionSet.h"

using EnumOptionSet = ::smoke::EnumOptionSet;



void register_smoke_EnumOptionSet(py::module_& module) {
auto cls_EnumOptionSet = py::enum_<EnumOptionSet>(module, "smoke_EnumOptionSet")
        .value("ONE", EnumOptionSet::ONE)
        .value("TWO", EnumOptionSet::TWO)
        .value("THREE", EnumOptionSet::THREE)
        ;


}
