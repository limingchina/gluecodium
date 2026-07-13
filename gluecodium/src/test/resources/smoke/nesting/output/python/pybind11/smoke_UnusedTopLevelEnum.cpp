

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/UnusedTopLevelEnum.h"

void register_UnusedTopLevelEnum(py::module_& module) {
    py::enum_<UnusedTopLevelEnum>(module, "UnusedTopLevelEnum")
        .value("DOESNT_WORK", UnusedTopLevelEnum::DOESNT_WORK)
        .value("CRASHED_ANYWAY", UnusedTopLevelEnum::CRASHED_ANYWAY)
        ;
}

