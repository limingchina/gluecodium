

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DefaultsWithFcStruct.h"
#include "smoke/FcStruct.h"

void register_DefaultsWithFcStruct(py::module_& module) {
    py::class_<DefaultsWithFcStruct>(module, "DefaultsWithFcStruct")
        .def_readwrite("struct_field", &DefaultsWithFcStruct::struct_field)
        ;
}

