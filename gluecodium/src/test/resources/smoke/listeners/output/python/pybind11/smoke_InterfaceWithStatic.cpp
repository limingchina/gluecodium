

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/InterfaceWithStatic.h"
#include "string"

void register_InterfaceWithStatic(py::module_& module) {
    py::class_<InterfaceWithStatic, std::shared_ptr<InterfaceWithStatic>>(module, "InterfaceWithStatic")
        .def("regular_function", &InterfaceWithStatic::regular_function)
        .def("static_function", &InterfaceWithStatic::static_function)
        .def_property("regular_property", &InterfaceWithStatic::get_regular_property)
        .def_property("static_property", &InterfaceWithStatic::get_static_property)
        ;
}

