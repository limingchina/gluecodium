

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SomeSkippedEnum.h"

void register_SomeSkippedEnum(py::module_& module) {
    py::enum_<SomeSkippedEnum>(module, "SomeSkippedEnum")
        .value("FOO", SomeSkippedEnum::FOO)
        ;
}

