

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SimpleClass.h"
#include "memory"
#include "string"

void register_SimpleClass(py::module_& module) {
    py::class_<SimpleClass>(module, "SimpleClass")
        .def("get_string_value", &SimpleClass::get_string_value)
        .def("use_simple_class", &SimpleClass::use_simple_class, py::arg("input"))
        ;
}

