

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/MultipleAttributesKotlin.h"

void register_MultipleAttributesKotlin(py::module_& module) {
    py::class_<MultipleAttributesKotlin>(module, "MultipleAttributesKotlin")
        .def("no_lists2", &MultipleAttributesKotlin::no_lists2)
        .def("no_lists3", &MultipleAttributesKotlin::no_lists3)
        .def("list_first", &MultipleAttributesKotlin::list_first)
        .def("list_second", &MultipleAttributesKotlin::list_second)
        .def("two_lists", &MultipleAttributesKotlin::two_lists)
        ;
}

