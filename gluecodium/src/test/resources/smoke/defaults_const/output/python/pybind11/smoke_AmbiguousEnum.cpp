

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
#include "smoke/AmbiguousEnum.h"

using AmbiguousEnum = ::smoke::AmbiguousEnum;



void register_smoke_AmbiguousEnum(py::module_& module) {
auto cls_AmbiguousEnum = py::enum_<AmbiguousEnum>(module, "smoke_AmbiguousEnum")
        .value("DISABLED", AmbiguousEnum::DISABLED)
        ;


}
