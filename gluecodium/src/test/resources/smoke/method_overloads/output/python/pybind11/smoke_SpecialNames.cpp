

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SpecialNames.h"
#include "memory"
#include "string"

void register_SpecialNames(py::module_& module) {
    py::class_<SpecialNames>(module, "SpecialNames")
        .def("create", &SpecialNames::create)
        .def("release", &SpecialNames::release)
        .def("create_proxy", &SpecialNames::create_proxy)
        .def("_uppercase", &SpecialNames::_uppercase)
        .def("make", &SpecialNames::make, py::arg("result"))
        ;
}

