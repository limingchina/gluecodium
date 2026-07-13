

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/NonEquatableClass.h"
#include "smoke/NonEquatableInterface.h"
#include "smoke/SimpleEquatableStruct.h"
#include "memory"

void register_SimpleEquatableStruct(py::module_& module) {
    py::class_<SimpleEquatableStruct>(module, "SimpleEquatableStruct")
        .def_readwrite("class_field", &SimpleEquatableStruct::class_field)
        .def_readwrite("interface_field", &SimpleEquatableStruct::interface_field)
        .def_readwrite("nullable_class_field", &SimpleEquatableStruct::nullable_class_field)
        .def_readwrite("nullable_interface_field", &SimpleEquatableStruct::nullable_interface_field)
        ;
}

