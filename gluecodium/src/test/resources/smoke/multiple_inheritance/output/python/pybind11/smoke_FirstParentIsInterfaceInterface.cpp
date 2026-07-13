

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FirstParentIsInterfaceInterface.h"
#include "string"

void register_FirstParentIsInterfaceInterface(py::module_& module) {
    py::class_<FirstParentIsInterfaceInterface, std::shared_ptr<FirstParentIsInterfaceInterface>>(module, "FirstParentIsInterfaceInterface")
        .def("child_function", &FirstParentIsInterfaceInterface::child_function)
        .def_property("child_property", &FirstParentIsInterfaceInterface::get_child_property)
        ;
}

