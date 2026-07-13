

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SimpleInterface.h"
#include "memory"
#include "string"

void register_SimpleInterface(py::module_& module) {
    py::class_<SimpleInterface, std::shared_ptr<SimpleInterface>>(module, "SimpleInterface")
        .def("get_string_value", &SimpleInterface::get_string_value)
        .def("use_simple_interface", &SimpleInterface::use_simple_interface, py::arg("input"))
        ;
}

