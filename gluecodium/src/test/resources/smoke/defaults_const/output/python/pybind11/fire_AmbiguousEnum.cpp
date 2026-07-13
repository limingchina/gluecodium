

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "fire/AmbiguousEnum.h"

void register_AmbiguousEnum(py::module_& module) {
    py::enum_<AmbiguousEnum>(module, "AmbiguousEnum")
        .value("DISABLED", AmbiguousEnum::DISABLED)
        ;
}

