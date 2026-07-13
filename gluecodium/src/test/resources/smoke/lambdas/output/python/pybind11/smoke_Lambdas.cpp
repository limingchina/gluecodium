

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/Lambdas.h"
#include "cstdint"
#include "functional"
#include "optional"
#include "string"
#include "unordered_map"
#include "vector"

void register_Lambdas(py::module_& module) {
    py::class_<Lambdas>(module, "Lambdas")
        .def("deconfuse", &Lambdas::deconfuse, py::arg("value"), py::arg("confuser"))
        .def("fuse", &Lambdas::fuse, py::arg("items"), py::arg("callback"))
        ;
}

