

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkipTagsInKotlin.h"

void register_SkipTagsInKotlin(py::module_& module) {
    py::class_<SkipTagsInKotlin, std::shared_ptr<SkipTagsInKotlin>>(module, "SkipTagsInKotlin")
        .def("skip_tagged", &SkipTagsInKotlin::skip_tagged)
        .def("dont_skip_tagged", &SkipTagsInKotlin::dont_skip_tagged)
        .def("skip_tagged_list", &SkipTagsInKotlin::skip_tagged_list)
        ;
}

