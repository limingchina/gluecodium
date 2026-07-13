

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/IncludableStruct.h"
#include "string"

void register_IncludableStruct(py::module_& module) {
    py::class_<IncludableStruct>(module, "IncludableStruct")
        .def_readwrite("field", &IncludableStruct::field)
        ;
}

