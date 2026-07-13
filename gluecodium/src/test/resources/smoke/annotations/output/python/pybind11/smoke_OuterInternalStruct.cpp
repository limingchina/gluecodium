

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/OuterInternalStruct.h"
#include "cstdint"

void register_OuterInternalStruct(py::module_& module) {
    py::class_<OuterInternalStruct>(module, "OuterInternalStruct")
        .def_readwrite("some_field", &OuterInternalStruct::some_field)
        ;
}

