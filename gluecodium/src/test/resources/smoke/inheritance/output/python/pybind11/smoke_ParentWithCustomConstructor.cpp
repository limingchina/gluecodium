

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ParentWithCustomConstructor.h"
#include "memory"

void register_ParentWithCustomConstructor(py::module_& module) {
    py::class_<ParentWithCustomConstructor>(module, "ParentWithCustomConstructor")
        .def("create", &ParentWithCustomConstructor::create)
        ;
}

