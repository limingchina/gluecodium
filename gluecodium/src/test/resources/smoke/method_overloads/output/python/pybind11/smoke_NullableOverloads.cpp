

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/NullableOverloads.h"
#include "optional"
#include "string"

void register_NullableOverloads(py::module_& module) {
    py::class_<NullableOverloads>(module, "NullableOverloads")
        .def("foo", &NullableOverloads::foo, py::arg("input"))
        .def("foo", &NullableOverloads::foo, py::arg("input"))
        ;
}

