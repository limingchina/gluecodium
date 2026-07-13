

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/MultipleAttributesDart.h"

void register_MultipleAttributesDart(py::module_& module) {
    py::class_<MultipleAttributesDart>(module, "MultipleAttributesDart")
        .def("no_lists2", &MultipleAttributesDart::no_lists2)
        .def("no_lists3", &MultipleAttributesDart::no_lists3)
        .def("list_first", &MultipleAttributesDart::list_first)
        .def("list_second", &MultipleAttributesDart::list_second)
        .def("two_lists", &MultipleAttributesDart::two_lists)
        ;
}

