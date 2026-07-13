

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/OuterClassWithInheritance.h"
#include "string"

void register_OuterClassWithInheritance(py::module_& module) {
    py::class_<OuterClassWithInheritance>(module, "OuterClassWithInheritance")
        .def("foo", &OuterClassWithInheritance::foo, py::arg("input"))
        ;
}

