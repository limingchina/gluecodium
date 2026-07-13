

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FooBarEnum.h"

void register_FooBarEnum(py::module_& module) {
    py::enum_<FooBarEnum>(module, "FooBarEnum")
        .value("FOO", FooBarEnum::FOO)
        .value("BAR", FooBarEnum::BAR)
        .value("BAZ", FooBarEnum::BAZ)
        ;
}

