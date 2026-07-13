

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkipTagsInJava.h"

void register_SkipTagsInJava(py::module_& module) {
    py::class_<SkipTagsInJava, std::shared_ptr<SkipTagsInJava>>(module, "SkipTagsInJava")
        .def("skip_tagged", &SkipTagsInJava::skip_tagged)
        .def("dont_skip_tagged", &SkipTagsInJava::dont_skip_tagged)
        .def("skip_tagged_list", &SkipTagsInJava::skip_tagged_list)
        ;
}

