

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FcStruct.h"
#include "string"

void register_FcStruct(py::module_& module) {
    py::class_<FcStruct>(module, "FcStruct")
        .def_readwrite("string_field", &FcStruct::string_field)
        ;
}

