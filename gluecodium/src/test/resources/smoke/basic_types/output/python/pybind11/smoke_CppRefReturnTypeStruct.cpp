

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/CppRefReturnTypeStruct.h"
#include "string"

void register_CppRefReturnTypeStruct(py::module_& module) {
    py::class_<CppRefReturnTypeStruct>(module, "CppRefReturnTypeStruct")
        .def("string_ref", &CppRefReturnTypeStruct::string_ref)
        ;
}

