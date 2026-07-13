

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DeclarationOrderWithFunctions.h"
#include "string"

void register_DeclarationOrderWithFunctions(py::module_& module) {
    py::class_<DeclarationOrderWithFunctions>(module, "DeclarationOrderWithFunctions")
        ;
}

