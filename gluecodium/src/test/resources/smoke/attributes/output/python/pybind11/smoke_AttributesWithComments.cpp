

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/AttributesWithComments.h"
#include "string"

void register_AttributesWithComments(py::module_& module) {
    py::class_<AttributesWithComments>(module, "AttributesWithComments")
        .def("very_fun", &AttributesWithComments::very_fun)
        .def_property("prop", &AttributesWithComments::get_prop)
        ;
}

