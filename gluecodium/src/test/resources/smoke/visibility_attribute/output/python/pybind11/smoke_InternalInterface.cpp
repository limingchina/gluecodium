

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/InternalInterface.h"
#include "string"

void register_InternalInterface(py::module_& module) {
    py::class_<InternalInterface, std::shared_ptr<InternalInterface>>(module, "InternalInterface")
        .def("foo_bar", &InternalInterface::foo_bar)
        .def_property("some_property_of_internal_interface", &InternalInterface::get_some_property_of_internal_interface)
        ;
}

