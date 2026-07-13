

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FirstParentIsNarrowClass.h"
#include "string"

void register_FirstParentIsNarrowClass(py::module_& module) {
    py::class_<FirstParentIsNarrowClass>(module, "FirstParentIsNarrowClass")
        .def("child_function", &FirstParentIsNarrowClass::child_function)
        .def_property("child_property", &FirstParentIsNarrowClass::get_child_property)
        ;
}

