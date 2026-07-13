

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkipTagsInDart.h"

void register_SkipTagsInDart(py::module_& module) {
    py::class_<SkipTagsInDart, std::shared_ptr<SkipTagsInDart>>(module, "SkipTagsInDart")
        .def("skip_tagged", &SkipTagsInDart::skip_tagged)
        .def("dont_skip_tagged", &SkipTagsInDart::dont_skip_tagged)
        .def("skip_tagged_list", &SkipTagsInDart::skip_tagged_list)
        ;
}

