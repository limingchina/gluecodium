

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
#include "smoke/UnusedTopLevelEnum.h"

using UnusedTopLevelEnum = ::smoke::UnusedTopLevelEnum;



void register_smoke_UnusedTopLevelEnum(py::module_& module) {
auto cls_UnusedTopLevelEnum = py::enum_<UnusedTopLevelEnum>(module, "smoke_UnusedTopLevelEnum")
        .value("DOESNT_WORK", UnusedTopLevelEnum::DOESNT_WORK)
        .value("CRASHED_ANYWAY", UnusedTopLevelEnum::CRASHED_ANYWAY)
        ;


}
