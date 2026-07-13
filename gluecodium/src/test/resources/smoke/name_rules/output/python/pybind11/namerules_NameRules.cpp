

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "VectorHash.h"
#include "namerules/NameRules.h"
#include "cstdint"
#include "memory"
#include "vector"

void register_NameRules(py::module_& module) {
    py::class_<NameRules>(module, "NameRules")
        .def("create", &NameRules::create)
        .def("some_method", &NameRules::someMethod, py::arg("some_argument"))
        .def_property("int_property", &NameRules::retrieve_int_property)
        .def_property("is_boolean_property", &NameRules::really_boolean_property)
        .def_property("struct_property", &NameRules::retrieve_struct_property)
        ;
}

