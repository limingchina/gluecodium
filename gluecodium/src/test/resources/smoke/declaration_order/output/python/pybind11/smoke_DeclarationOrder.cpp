

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DeclarationOrder.h"
#include "string"

void register_DeclarationOrder(py::module_& module) {
    py::class_<DeclarationOrder>(module, "DeclarationOrder")
        ;
}

