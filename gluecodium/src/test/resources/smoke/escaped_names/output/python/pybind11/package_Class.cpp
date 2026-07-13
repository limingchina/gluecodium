

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "package/Class.h"
#include "package/Types.h"
#include "memory"

void register_Class(py::module_& module) {
    py::class_<Class>(module, "Class")
        .def("constructor", &Class::constructor)
        .def("fun", &Class::fun, py::arg("double"))
        .def_property("property", &Class::get_property)
        ;
}

