

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ChildClassFromClassOverloads.h"
#include "string"

void register_ChildClassFromClassOverloads(py::module_& module) {
    py::class_<ChildClassFromClassOverloads>(module, "ChildClassFromClassOverloads")
        .def("foo", &ChildClassFromClassOverloads::foo, py::arg("input"))
        .def("foo", &ChildClassFromClassOverloads::foo, py::arg("input"))
        .def("bar", &ChildClassFromClassOverloads::bar, py::arg("input"))
        .def("bar", &ChildClassFromClassOverloads::bar, py::arg("input"))
        ;
}

