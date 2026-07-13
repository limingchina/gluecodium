

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ParentInterface.h"
#include "cstdint"

void register_ParentInterface(py::module_& module) {
    py::class_<ParentInterface, std::shared_ptr<ParentInterface>>(module, "ParentInterface")
        .def("foo", &ParentInterface::foo)
        .def("foo", &ParentInterface::foo, py::arg("input"))
        .def("bar", &ParentInterface::bar)
        .def("baz", &ParentInterface::baz)
        ;
}

