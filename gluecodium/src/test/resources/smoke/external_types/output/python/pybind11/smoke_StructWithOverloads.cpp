

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "include/ExternalTypes.h"
#include "cstdint"
#include "string"

void register_StructWithOverloads(py::module_& module) {
    py::class_<external::ClassWithOverloads::StructWithOverloads>(module, "StructWithOverloads")
        .def_readwrite("overloaded_accessors", &external::ClassWithOverloads::StructWithOverloads::overloadedAccessors)
        .def("overloaded_method", &external::ClassWithOverloads::StructWithOverloads::overloadedMethod)
        .def("overloaded_method", &external::ClassWithOverloads::StructWithOverloads::overloadedMethod, py::arg("input"))
        .def("overloaded_method", &external::ClassWithOverloads::StructWithOverloads::overloadedMethod, py::arg("input_string"), py::arg("input_bool"))
        ;
}

