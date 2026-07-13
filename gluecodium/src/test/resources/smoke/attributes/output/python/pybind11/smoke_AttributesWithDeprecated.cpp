

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/AttributesWithDeprecated.h"
#include "string"

void register_AttributesWithDeprecated(py::module_& module) {
    py::class_<AttributesWithDeprecated>(module, "AttributesWithDeprecated")
        .def("very_fun", &AttributesWithDeprecated::very_fun)
        .def_property("prop", &AttributesWithDeprecated::get_prop)
        ;
}

