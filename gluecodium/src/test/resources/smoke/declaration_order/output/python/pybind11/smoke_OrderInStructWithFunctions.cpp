

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/OrderInStructWithFunctions.h"
#include "string"

void register_OrderInStructWithFunctions(py::module_& module) {
    py::class_<OrderInStructWithFunctions>(module, "OrderInStructWithFunctions")
        .def_readwrite("some_field", &OrderInStructWithFunctions::some_field)
        .def("do_stuff", &OrderInStructWithFunctions::do_stuff, py::arg("struct_foo"))
        ;
}

