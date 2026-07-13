

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SkippedEverywhereEnum.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SkippedEverywhereEnum = ::gluecodium::smoke::SkippedEverywhereEnum;

void register_SkippedEverywhereEnum(py::module_& module) {
    py::enum_<SkippedEverywhereEnum>(module, "SkippedEverywhereEnum")
        .value("NOTHING_TO_SEE_HERE", SkippedEverywhereEnum::NOTHING_TO_SEE_HERE)
        ;
}

