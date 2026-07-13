

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/OuterInternalEnum.h"

void register_OuterInternalEnum(py::module_& module) {
    py::enum_<OuterInternalEnum>(module, "OuterInternalEnum")
        .value("FIRST", OuterInternalEnum::FIRST)
        .value("SECOND", OuterInternalEnum::SECOND)
        ;
}

