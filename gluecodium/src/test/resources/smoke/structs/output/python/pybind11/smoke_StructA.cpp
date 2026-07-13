

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/StructA.h"
#include "smoke/StructB.h"
#include "vector"

void register_StructA(py::module_& module) {
    py::class_<StructA>(module, "StructA")
        .def_readwrite("field", &StructA::field)
        ;
}

