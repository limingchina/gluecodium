

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ChildClassFromClass.h"
#include "smoke/ParentClass.h"
#include "smoke/ParentWithClassReferences.h"
#include "memory"

void register_ParentWithClassReferences(py::module_& module) {
    py::class_<ParentWithClassReferences, std::shared_ptr<ParentWithClassReferences>>(module, "ParentWithClassReferences")
        .def("class_function", &ParentWithClassReferences::class_function)
        .def_property("class_property", &ParentWithClassReferences::get_class_property)
        ;
}

