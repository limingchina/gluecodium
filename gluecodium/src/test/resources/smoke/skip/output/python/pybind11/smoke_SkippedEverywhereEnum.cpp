

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkippedEverywhereEnum.h"

void register_SkippedEverywhereEnum(py::module_& module) {
    py::enum_<SkippedEverywhereEnum>(module, "SkippedEverywhereEnum")
        .value("NOTHING_TO_SEE_HERE", SkippedEverywhereEnum::NOTHING_TO_SEE_HERE)
        ;
}

