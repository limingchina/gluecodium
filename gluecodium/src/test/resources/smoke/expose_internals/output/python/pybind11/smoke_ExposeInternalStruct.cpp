

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ExposeInternalStruct.h"
#include "string"

void register_ExposeInternalStruct(py::module_& module) {
    py::class_<ExposeInternalStruct>(module, "ExposeInternalStruct")
        .def_readwrite("field", &ExposeInternalStruct::field)
        ;
}

