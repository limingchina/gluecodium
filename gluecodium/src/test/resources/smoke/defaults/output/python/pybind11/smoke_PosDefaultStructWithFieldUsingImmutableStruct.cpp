

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ImmutableStructWithDefaults.h"
#include "smoke/PosDefaultStructWithFieldUsingImmutableStruct.h"

void register_PosDefaultStructWithFieldUsingImmutableStruct(py::module_& module) {
    py::class_<PosDefaultStructWithFieldUsingImmutableStruct>(module, "PosDefaultStructWithFieldUsingImmutableStruct")
        .def_readwrite("some_field1", &PosDefaultStructWithFieldUsingImmutableStruct::some_field1)
        ;
}

