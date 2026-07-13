

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DummyStruct.h"
#include "string"

void register_DummyStruct(py::module_& module) {
    py::class_<DummyStruct>(module, "DummyStruct")
        .def_readwrite("string_field", &DummyStruct::string_field)
        ;
}

