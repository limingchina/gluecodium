

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ParentClass.h"
#include "string"

void register_ParentClass(py::module_& module) {
    py::class_<ParentClass>(module, "ParentClass")
        .def("parent_fun", &ParentClass::parent_fun)
        .def_property("parent_property", &ParentClass::get_parent_property)
        ;
}

