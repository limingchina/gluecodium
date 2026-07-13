

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/AttributesInterface.h"
#include "string"

void register_AttributesInterface(py::module_& module) {
    py::class_<AttributesInterface, std::shared_ptr<AttributesInterface>>(module, "AttributesInterface")
        .def("very_fun", &AttributesInterface::very_fun, py::arg("param"))
        .def_property("prop", &AttributesInterface::get_prop)
        ;
}

