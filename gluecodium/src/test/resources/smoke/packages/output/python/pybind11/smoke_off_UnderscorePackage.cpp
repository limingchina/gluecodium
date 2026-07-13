

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke_off/UnderscorePackage.h"
#include "string"

void register_UnderscorePackage(py::module_& module) {
    py::class_<UnderscorePackage>(module, "UnderscorePackage")
        .def("basic_method", &UnderscorePackage::basic_method, py::arg("input_string"))
        ;
}

