

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ExposeEnum.h"

void register_ExposeEnum(py::module_& module) {
    py::enum_<ExposeEnum>(module, "ExposeEnum")
        .value("FOO", ExposeEnum::FOO)
        ;
}

