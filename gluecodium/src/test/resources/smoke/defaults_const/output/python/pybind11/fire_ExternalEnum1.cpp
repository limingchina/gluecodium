

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "foo/AlienEnum1.h"

void register_ExternalEnum1(py::module_& module) {
    py::enum_<foo::AlienEnum1>(module, "ExternalEnum1")
        .value("ENABLED", foo::AlienEnum1::ENABLED)
        .value("DISABLED", foo::AlienEnum1::DISABLED)
        ;
}

