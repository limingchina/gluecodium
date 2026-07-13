

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EnableTagsInDart.h"

void register_EnableTagsInDart(py::module_& module) {
    py::class_<EnableTagsInDart, std::shared_ptr<EnableTagsInDart>>(module, "EnableTagsInDart")
        .def("enable_tagged", &EnableTagsInDart::enable_tagged)
        .def("dont_enable_tagged", &EnableTagsInDart::dont_enable_tagged)
        .def("enable_tagged_list", &EnableTagsInDart::enable_tagged_list)
        ;
}

