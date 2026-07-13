

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EnableTagsInJava.h"

void register_EnableTagsInJava(py::module_& module) {
    py::class_<EnableTagsInJava, std::shared_ptr<EnableTagsInJava>>(module, "EnableTagsInJava")
        .def("enable_tagged", &EnableTagsInJava::enable_tagged)
        .def("dont_enable_tagged", &EnableTagsInJava::dont_enable_tagged)
        .def("enable_tagged_list", &EnableTagsInJava::enable_tagged_list)
        ;
}

