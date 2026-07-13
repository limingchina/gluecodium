

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ChildWithCustomConstructor.h"
#include "memory"

void register_ChildWithCustomConstructor(py::module_& module) {
    py::class_<ChildWithCustomConstructor>(module, "ChildWithCustomConstructor")
        .def("make", &ChildWithCustomConstructor::make)
        ;
}

