

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ChildInterfaceOverloads.h"
#include "string"

void register_ChildInterfaceOverloads(py::module_& module) {
    py::class_<ChildInterfaceOverloads, std::shared_ptr<ChildInterfaceOverloads>>(module, "ChildInterfaceOverloads")
        .def("foo", &ChildInterfaceOverloads::foo, py::arg("input"))
        .def("bar", &ChildInterfaceOverloads::bar, py::arg("input"))
        ;
}

