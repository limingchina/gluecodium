

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/fooInterface.h"
#include "smoke/fooTypes.h"
#include "cstdint"
#include "memory"
#include "string"

void register_PlatformNamesInterface(py::module_& module) {
    py::class_<fooInterface>(module, "PlatformNamesInterface")
        .def("basic_method", &fooInterface::FooMethod, py::arg("basic_parameter"))
        .def("create", &fooInterface::make, py::arg("basic_parameter"))
        .def_property("basic_property", &fooInterface::GET_FOO_PROPERTY)
        ;
}

