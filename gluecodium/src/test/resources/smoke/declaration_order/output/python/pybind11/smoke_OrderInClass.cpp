

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/OrderInClass.h"
#include "string"

void register_OrderInClass(py::module_& module) {
    py::class_<OrderInClass>(module, "OrderInClass")
        ;
}

