

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ChildClassFromInterfaceOverloads.h"
#include "cstdint"
#include "string"

void register_ChildClassFromInterfaceOverloads(py::module_& module) {
    py::class_<ChildClassFromInterfaceOverloads>(module, "ChildClassFromInterfaceOverloads")
        .def("foo", &ChildClassFromInterfaceOverloads::foo, py::arg("input"))
        .def("foo", &ChildClassFromInterfaceOverloads::foo, py::arg("input"))
        .def("bar", &ChildClassFromInterfaceOverloads::bar, py::arg("input"))
        .def("bar", &ChildClassFromInterfaceOverloads::bar, py::arg("input"))
        ;
}

