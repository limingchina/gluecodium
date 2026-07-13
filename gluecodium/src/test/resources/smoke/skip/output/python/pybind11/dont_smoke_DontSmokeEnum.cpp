

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "dont/smoke/DontSmokeEnum.h"

void register_DontSmokeEnum(py::module_& module) {
    py::enum_<DontSmokeEnum>(module, "DontSmokeEnum")
        .value("FOO", DontSmokeEnum::FOO)
        ;
}

