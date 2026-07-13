

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/GrandChildInterface.h"

void register_GrandChildInterface(py::module_& module) {
    py::class_<GrandChildInterface, std::shared_ptr<GrandChildInterface>>(module, "GrandChildInterface")
        .def("grand_child_method", &GrandChildInterface::grand_child_method)
        ;
}

