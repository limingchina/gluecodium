

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "fire/SomeStruct.h"
#include "cstdint"

void register_SomeStruct(py::module_& module) {
    py::class_<SomeStruct>(module, "SomeStruct")
        .def_readwrite("int_field", &SomeStruct::int_field)
        ;
}

