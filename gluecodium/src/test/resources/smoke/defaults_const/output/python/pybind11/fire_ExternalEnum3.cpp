

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "foo/AlienEnum3.h"

void register_ExternalEnum3(py::module_& module) {
    py::enum_<foo::AlienEnum3>(module, "ExternalEnum3")
        .value("ENABLED", foo::AlienEnum3::ENABLED)
        .value("DISABLED", foo::AlienEnum3::DISABLED)
        ;
}

