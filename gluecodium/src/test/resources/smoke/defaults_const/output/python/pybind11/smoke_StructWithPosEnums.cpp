

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SomethingEnum.h"
#include "smoke/StructWithPosEnums.h"

void register_StructWithPosEnums(py::module_& module) {
    py::class_<StructWithPosEnums>(module, "StructWithPosEnums")
        .def_readwrite("first_field", &StructWithPosEnums::first_field)
        .def_readwrite("explicit_field", &StructWithPosEnums::explicit_field)
        .def_readwrite("last_field", &StructWithPosEnums::last_field)
        ;
}

