

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ParentInterface.h"
#include "string"

void register_ParentInterface(py::module_& module) {
    py::class_<ParentInterface, std::shared_ptr<ParentInterface>>(module, "ParentInterface")
        .def("root_method", &ParentInterface::root_method)
        .def_property("root_property", &ParentInterface::get_root_property)
        ;
}

