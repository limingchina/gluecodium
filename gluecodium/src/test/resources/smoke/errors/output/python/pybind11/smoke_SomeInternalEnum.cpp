

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SomeInternalEnum.h"

void register_SomeInternalEnum(py::module_& module) {
    py::enum_<SomeInternalEnum>(module, "SomeInternalEnum")
        .value("ONE", SomeInternalEnum::ONE)
        .value("TWO", SomeInternalEnum::TWO)
        .value("THREE", SomeInternalEnum::THREE)
        .value("SINGLE", SomeInternalEnum::SINGLE)
        ;
}

