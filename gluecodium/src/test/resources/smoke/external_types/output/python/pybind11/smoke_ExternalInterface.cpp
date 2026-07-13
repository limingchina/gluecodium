

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "foo/Bar.h"
#include "cstdint"
#include "string"

void register_ExternalInterface(py::module_& module) {
    py::class_<ExternalInterface, std::shared_ptr<ExternalInterface>>(module, "ExternalInterface")
        .def("some_method", &ExternalInterface::some_Method, py::arg("some_parameter"))
        .def_property("some_property", &ExternalInterface::get_Me)
        ;
}

