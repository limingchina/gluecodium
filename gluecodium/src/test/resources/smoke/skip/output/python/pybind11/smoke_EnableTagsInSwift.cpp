

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EnableTagsInSwift.h"

void register_EnableTagsInSwift(py::module_& module) {
    py::class_<EnableTagsInSwift, std::shared_ptr<EnableTagsInSwift>>(module, "EnableTagsInSwift")
        .def("enable_tagged", &EnableTagsInSwift::enable_tagged)
        .def("dont_enable_tagged", &EnableTagsInSwift::dont_enable_tagged)
        .def("enable_tagged_list", &EnableTagsInSwift::enable_tagged_list)
        ;
}

