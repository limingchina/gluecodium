

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "another/SomeCoolClassType.h"
#include "smoke/FirstParentIsInterfaceClass.h"
#include "memory"
#include "string"

void register_FirstParentIsInterfaceClass(py::module_& module) {
    py::class_<FirstParentIsInterfaceClass>(module, "FirstParentIsInterfaceClass")
        .def("child_function", &FirstParentIsInterfaceClass::child_function)
        .def_property("child_property", &FirstParentIsInterfaceClass::get_child_property)
        ;
}

