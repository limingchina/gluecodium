

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/OuterInterface.h"
#include "string"

void register_OuterInterface(py::module_& module) {
    py::class_<OuterInterface, std::shared_ptr<OuterInterface>>(module, "OuterInterface")
        .def("foo", &OuterInterface::foo, py::arg("input"))
        ;
}

