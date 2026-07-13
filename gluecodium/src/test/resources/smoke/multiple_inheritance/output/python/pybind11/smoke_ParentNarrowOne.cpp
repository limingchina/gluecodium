

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ParentNarrowOne.h"
#include "string"

void register_ParentNarrowOne(py::module_& module) {
    py::class_<ParentNarrowOne, std::shared_ptr<ParentNarrowOne>>(module, "ParentNarrowOne")
        .def("parent_function_one", &ParentNarrowOne::parent_function_one)
        .def_property("parent_property_one", &ParentNarrowOne::get_parent_property_one)
        ;
}

