

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/AttributesClass.h"
#include "string"

void register_AttributesClass(py::module_& module) {
    py::class_<AttributesClass>(module, "AttributesClass")
        .def("very_fun", &AttributesClass::very_fun, py::arg("param"))
        .def_property("prop", &AttributesClass::get_prop)
        ;
}

