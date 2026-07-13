

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SingleNamedConstructor.h"
#include "memory"

void register_SingleNamedConstructor(py::module_& module) {
    py::class_<SingleNamedConstructor>(module, "SingleNamedConstructor")
        .def("create", &SingleNamedConstructor::create)
        ;
}

