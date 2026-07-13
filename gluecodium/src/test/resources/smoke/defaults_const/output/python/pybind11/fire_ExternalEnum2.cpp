

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "foo/AlienEnum2.h"

void register_ExternalEnum2(py::module_& module) {
    py::enum_<foo::AlienEnum2>(module, "ExternalEnum2")
        .value("ENABLED", foo::AlienEnum2::ENABLED)
        .value("DISABLED", foo::AlienEnum2::DISABLED)
        ;
}

