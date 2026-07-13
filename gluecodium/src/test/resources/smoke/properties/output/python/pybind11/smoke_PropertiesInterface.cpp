

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/PropertiesInterface.h"

void register_PropertiesInterface(py::module_& module) {
    py::class_<PropertiesInterface, std::shared_ptr<PropertiesInterface>>(module, "PropertiesInterface")
        .def_property("struct_property", &PropertiesInterface::get_struct_property)
        ;
}

