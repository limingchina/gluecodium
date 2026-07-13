

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ChildClassFromInterface.h"
#include "string"

void register_ChildClassFromInterface(py::module_& module) {
    py::class_<ChildClassFromInterface>(module, "ChildClassFromInterface")
        .def("child_class_method", &ChildClassFromInterface::child_class_method)
        ;
}

