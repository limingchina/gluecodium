

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FreeEnum.h"

void register_FreeEnum(py::module_& module) {
    py::enum_<FreeEnum>(module, "FreeEnum")
        .value("FOO", FreeEnum::FOO)
        .value("BAR", FreeEnum::BAR)
        ;
}

