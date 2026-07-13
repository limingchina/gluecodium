

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ParentInterfaceWithBool.h"

void register_ParentInterfaceWithBool(py::module_& module) {
    py::class_<ParentInterfaceWithBool, std::shared_ptr<ParentInterfaceWithBool>>(module, "ParentInterfaceWithBool")
        .def("root_method", &ParentInterfaceWithBool::root_method, py::arg("input1"))
        ;
}

