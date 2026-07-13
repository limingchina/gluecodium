

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ParentClass.h"
#include "string"

void register_ParentClass(py::module_& module) {
    py::class_<ParentClass>(module, "ParentClass")
        .def("root_method", &ParentClass::root_method)
        .def_property("root_property", &ParentClass::get_root_property)
        ;
}

