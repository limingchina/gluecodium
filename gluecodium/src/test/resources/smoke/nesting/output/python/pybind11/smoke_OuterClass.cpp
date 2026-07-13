

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/OuterClass.h"
#include "string"

void register_OuterClass(py::module_& module) {
    py::class_<OuterClass>(module, "OuterClass")
        .def("foo", &OuterClass::foo, py::arg("input"))
        ;
}

