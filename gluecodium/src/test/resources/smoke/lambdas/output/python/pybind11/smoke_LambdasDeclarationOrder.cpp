

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/LambdasDeclarationOrder.h"
#include "functional"
#include "string"

void register_LambdasDeclarationOrder(py::module_& module) {
    py::class_<LambdasDeclarationOrder>(module, "LambdasDeclarationOrder")
        ;
}

