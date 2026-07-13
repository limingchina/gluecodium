

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ExposeInternalEnum.h"

void register_ExposeInternalEnum(py::module_& module) {
    py::enum_<ExposeInternalEnum>(module, "ExposeInternalEnum")
        .value("FOO", ExposeInternalEnum::FOO)
        ;
}

