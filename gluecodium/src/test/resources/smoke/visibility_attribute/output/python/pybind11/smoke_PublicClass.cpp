

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/PublicClass.h"
#include "string"

void register_PublicClass(py::module_& module) {
    py::class_<PublicClass>(module, "PublicClass")
        .def("internal_method", &PublicClass::internal_method, py::arg("input"))
        .def_property("internal_struct_property", &PublicClass::get_internal_struct_property)
        ;
}

