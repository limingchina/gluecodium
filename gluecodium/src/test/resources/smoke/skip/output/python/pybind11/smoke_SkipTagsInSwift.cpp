

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkipTagsInSwift.h"

void register_SkipTagsInSwift(py::module_& module) {
    py::class_<SkipTagsInSwift, std::shared_ptr<SkipTagsInSwift>>(module, "SkipTagsInSwift")
        .def("skip_tagged", &SkipTagsInSwift::skip_tagged)
        .def("dont_skip_tagged", &SkipTagsInSwift::dont_skip_tagged)
        .def("skip_tagged_list", &SkipTagsInSwift::skip_tagged_list)
        ;
}

