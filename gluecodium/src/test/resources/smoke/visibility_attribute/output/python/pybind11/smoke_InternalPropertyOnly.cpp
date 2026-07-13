

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/InternalPropertyOnly.h"

void register_InternalPropertyOnly(py::module_& module) {
    py::class_<InternalPropertyOnly>(module, "InternalPropertyOnly")
        .def_property("foo", &InternalPropertyOnly::get_foo)
        ;
}

