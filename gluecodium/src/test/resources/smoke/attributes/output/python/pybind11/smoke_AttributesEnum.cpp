

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/AttributesEnum.h"

void register_AttributesEnum(py::module_& module) {
    py::enum_<AttributesEnum>(module, "AttributesEnum")
        .value("NOPE", AttributesEnum::NOPE)
        ;
}

