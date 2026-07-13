

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/IncludableEnum.h"

void register_IncludableEnum(py::module_& module) {
    py::enum_<IncludableEnum>(module, "IncludableEnum")
        .value("FOO", IncludableEnum::FOO)
        ;
}

