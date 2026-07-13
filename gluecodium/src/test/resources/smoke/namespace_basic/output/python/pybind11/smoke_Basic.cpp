

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "root/space/smoke/Basic.h"
#include "string"

void register_Basic(py::module_& module) {
    py::class_<Basic>(module, "Basic")
        .def("basic_method", &Basic::basic_method, py::arg("input_string"))
        ;
}

