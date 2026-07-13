

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "foo/AlienEnum4.h"

void register_ExternalEnum4(py::module_& module) {
    py::enum_<foo::AlienEnum4>(module, "ExternalEnum4")
        .value("ENABLED", foo::AlienEnum4::ENABLED)
        .value("DISABLED", foo::AlienEnum4::DISABLED)
        ;
}

