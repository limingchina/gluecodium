

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ExposeStruct.h"
#include "string"

void register_ExposeStruct(py::module_& module) {
    py::class_<ExposeStruct>(module, "ExposeStruct")
        .def_readwrite("field", &ExposeStruct::field)
        ;
}

