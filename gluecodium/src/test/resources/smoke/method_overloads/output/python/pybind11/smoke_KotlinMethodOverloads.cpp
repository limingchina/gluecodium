

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/KotlinMethodOverloads.h"
#include "string"
#include "vector"

void register_KotlinMethodOverloads(py::module_& module) {
    py::class_<KotlinMethodOverloads>(module, "KotlinMethodOverloads")
        .def("one", &KotlinMethodOverloads::one, py::arg("input"))
        .def("two", &KotlinMethodOverloads::two, py::arg("input"))
        ;
}

