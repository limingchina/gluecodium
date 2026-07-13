

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EnableTagsInKotlin.h"

void register_EnableTagsInKotlin(py::module_& module) {
    py::class_<EnableTagsInKotlin, std::shared_ptr<EnableTagsInKotlin>>(module, "EnableTagsInKotlin")
        .def("enable_tagged", &EnableTagsInKotlin::enable_tagged)
        .def("dont_enable_tagged", &EnableTagsInKotlin::dont_enable_tagged)
        .def("enable_tagged_list", &EnableTagsInKotlin::enable_tagged_list)
        ;
}

