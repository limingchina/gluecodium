

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/OrderInStruct.h"
#include "string"

void register_OrderInStruct(py::module_& module) {
    py::class_<OrderInStruct>(module, "OrderInStruct")
        .def_readwrite("struct_field", &OrderInStruct::struct_field)
        .def_readwrite("enum_field", &OrderInStruct::enum_field)
        ;
}

