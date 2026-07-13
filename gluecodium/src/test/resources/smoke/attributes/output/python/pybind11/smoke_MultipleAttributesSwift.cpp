

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/MultipleAttributesSwift.h"

void register_MultipleAttributesSwift(py::module_& module) {
    py::class_<MultipleAttributesSwift>(module, "MultipleAttributesSwift")
        .def("no_lists2", &MultipleAttributesSwift::no_lists2)
        .def("no_lists3", &MultipleAttributesSwift::no_lists3)
        .def("list_first", &MultipleAttributesSwift::list_first)
        .def("list_second", &MultipleAttributesSwift::list_second)
        .def("two_lists", &MultipleAttributesSwift::two_lists)
        ;
}

