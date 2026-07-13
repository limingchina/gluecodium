

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FirstParentIsNarrowInterface.h"
#include "string"

void register_FirstParentIsNarrowInterface(py::module_& module) {
    py::class_<FirstParentIsNarrowInterface, std::shared_ptr<FirstParentIsNarrowInterface>>(module, "FirstParentIsNarrowInterface")
        .def("child_function", &FirstParentIsNarrowInterface::child_function)
        .def_property("child_property", &FirstParentIsNarrowInterface::get_child_property)
        ;
}

