

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ChildClassFromClass.h"

void register_ChildClassFromClass(py::module_& module) {
    py::class_<ChildClassFromClass>(module, "ChildClassFromClass")
        .def("child_class_method", &ChildClassFromClass::child_class_method)
        ;
}

