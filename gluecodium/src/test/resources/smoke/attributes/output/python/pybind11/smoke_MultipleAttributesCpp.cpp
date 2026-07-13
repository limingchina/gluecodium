

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/MultipleAttributesCpp.h"

void register_MultipleAttributesCpp(py::module_& module) {
    py::class_<MultipleAttributesCpp>(module, "MultipleAttributesCpp")
        .def("no_lists2", &MultipleAttributesCpp::no_lists2)
        .def("no_lists3", &MultipleAttributesCpp::no_lists3)
        .def("list_first", &MultipleAttributesCpp::list_first)
        .def("list_second", &MultipleAttributesCpp::list_second)
        .def("two_lists", &MultipleAttributesCpp::two_lists)
        ;
}

