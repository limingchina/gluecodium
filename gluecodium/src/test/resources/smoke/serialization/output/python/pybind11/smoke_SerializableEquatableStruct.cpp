

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SerializableEquatableStruct.h"
#include "string"

void register_SerializableEquatableStruct(py::module_& module) {
    py::class_<SerializableEquatableStruct>(module, "SerializableEquatableStruct")
        .def_readwrite("foo_field", &SerializableEquatableStruct::foo_field)
        ;
}

