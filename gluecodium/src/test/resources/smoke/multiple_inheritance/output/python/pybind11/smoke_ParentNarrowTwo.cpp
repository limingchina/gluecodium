

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ParentNarrowTwo.h"
#include "string"

void register_ParentNarrowTwo(py::module_& module) {
    py::class_<ParentNarrowTwo, std::shared_ptr<ParentNarrowTwo>>(module, "ParentNarrowTwo")
        .def("parent_function_two", &ParentNarrowTwo::parent_function_two)
        .def_property("parent_property_two", &ParentNarrowTwo::get_parent_property_two)
        ;
}

