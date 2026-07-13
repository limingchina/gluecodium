

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "foo/Bar.h"

void register_StandaloneExternalEnum(py::module_& module) {
    py::enum_<StandaloneExternalEnum>(module, "StandaloneExternalEnum")
        .value("FOO", StandaloneExternalEnum::foo)
        ;
}

