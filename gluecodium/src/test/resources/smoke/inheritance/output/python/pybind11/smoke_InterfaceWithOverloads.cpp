

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/InterfaceWithOverloads.h"
#include "string"

void register_InterfaceWithOverloads(py::module_& module) {
    py::class_<InterfaceWithOverloads, std::shared_ptr<InterfaceWithOverloads>>(module, "InterfaceWithOverloads")
        .def("parent_method", &InterfaceWithOverloads::parent_method)
        .def("parent_method", &InterfaceWithOverloads::parent_method, py::arg("input"))
        ;
}

