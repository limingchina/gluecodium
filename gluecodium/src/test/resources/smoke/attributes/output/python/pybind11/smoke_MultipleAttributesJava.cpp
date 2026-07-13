

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/MultipleAttributesJava.h"

void register_MultipleAttributesJava(py::module_& module) {
    py::class_<MultipleAttributesJava>(module, "MultipleAttributesJava")
        .def("no_lists2", &MultipleAttributesJava::no_lists2)
        .def("no_lists3", &MultipleAttributesJava::no_lists3)
        .def("list_first", &MultipleAttributesJava::list_first)
        .def("list_second", &MultipleAttributesJava::list_second)
        .def("two_lists", &MultipleAttributesJava::two_lists)
        ;
}

