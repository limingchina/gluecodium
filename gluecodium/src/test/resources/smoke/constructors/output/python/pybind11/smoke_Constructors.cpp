

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/Constructors.h"
#include "cstdint"
#include "memory"
#include "string"
#include "vector"

void register_Constructors(py::module_& module) {
    py::class_<Constructors>(module, "Constructors")
        .def("create", &Constructors::create)
        .def("create", &Constructors::create, py::arg("other"))
        .def("create", &Constructors::create, py::arg("foo"), py::arg("bar"))
        .def("create", &Constructors::create, py::arg("input"))
        .def("create", &Constructors::create, py::arg("input"))
        .def("create", &Constructors::create, py::arg("input"))
        ;
}

