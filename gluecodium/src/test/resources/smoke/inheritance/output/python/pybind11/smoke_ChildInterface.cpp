

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ChildInterface.h"

void register_ChildInterface(py::module_& module) {
    py::class_<ChildInterface, std::shared_ptr<ChildInterface>>(module, "ChildInterface")
        .def("child_method", &ChildInterface::child_method)
        ;
}

