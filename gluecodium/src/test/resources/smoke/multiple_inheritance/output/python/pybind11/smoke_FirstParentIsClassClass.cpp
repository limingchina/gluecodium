

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FirstParentIsClassClass.h"
#include "string"

void register_FirstParentIsClassClass(py::module_& module) {
    py::class_<FirstParentIsClassClass>(module, "FirstParentIsClassClass")
        .def("child_function", &FirstParentIsClassClass::child_function)
        .def_property("child_property", &FirstParentIsClassClass::get_child_property)
        ;
}

