

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "another/SomeCoolClassType.h"
#include "smoke/ParentInterface.h"
#include "memory"
#include "string"

void register_ParentInterface(py::module_& module) {
    py::class_<ParentInterface, std::shared_ptr<ParentInterface>>(module, "ParentInterface")
        .def("parent_function", &ParentInterface::parent_function)
        .def("some_function_that_uses_type_from_another_package", &ParentInterface::some_function_that_uses_type_from_another_package, py::arg("some_param"))
        .def_property("parent_property", &ParentInterface::get_parent_property)
        ;
}

