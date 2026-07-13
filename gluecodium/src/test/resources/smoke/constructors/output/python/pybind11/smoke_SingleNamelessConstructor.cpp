

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SingleNamelessConstructor.h"
#include "memory"

void register_SingleNamelessConstructor(py::module_& module) {
    py::class_<SingleNamelessConstructor>(module, "SingleNamelessConstructor")
        .def("create", &SingleNamelessConstructor::create)
        ;
}

