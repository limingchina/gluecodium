

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "foo/Bar.h"
#include "cstdint"
#include "string"

void register_ExternalClass(py::module_& module) {
    py::class_<::fire::Baz>(module, "ExternalClass")
        .def("some_method", &::fire::Baz::some_Method, py::arg("some_parameter"))
        .def_property("some_property", &::fire::Baz::get_Me)
        ;
}

