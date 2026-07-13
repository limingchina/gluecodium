

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/StructWithConstMethod.h"
#include "string"

void register_StructWithConstMethod(py::module_& module) {
    py::class_<StructWithConstMethod>(module, "StructWithConstMethod")
        .def_readwrite("string_field", &StructWithConstMethod::string_field)
        .def("double_const", &StructWithConstMethod::double_const)
        ;
}

