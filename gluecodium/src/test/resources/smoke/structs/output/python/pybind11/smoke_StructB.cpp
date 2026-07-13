

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/StructA.h"
#include "smoke/StructB.h"
#include "vector"

void register_StructB(py::module_& module) {
    py::class_<StructB>(module, "StructB")
        .def_readwrite("field", &StructB::field)
        ;
}

