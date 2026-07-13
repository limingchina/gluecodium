

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/JavaMethodOverloads.h"
#include "string"
#include "vector"

void register_JavaMethodOverloads(py::module_& module) {
    py::class_<JavaMethodOverloads>(module, "JavaMethodOverloads")
        .def("one", &JavaMethodOverloads::one, py::arg("input"))
        .def("two", &JavaMethodOverloads::two, py::arg("input"))
        ;
}

