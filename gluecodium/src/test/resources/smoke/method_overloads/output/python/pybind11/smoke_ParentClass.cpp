

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ParentClass.h"
#include "cstdint"

void register_ParentClass(py::module_& module) {
    py::class_<ParentClass>(module, "ParentClass")
        .def("foo", &ParentClass::foo)
        .def("foo", &ParentClass::foo, py::arg("input"))
        .def("bar", &ParentClass::bar)
        .def("baz", &ParentClass::baz)
        ;
}

