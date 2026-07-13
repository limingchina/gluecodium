

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/StructsWithMethodsInterface.h"
#include "smoke/ValidationUtils.h"
#include "string"

void register_StructsWithMethodsInterface(py::module_& module) {
    py::class_<StructsWithMethodsInterface>(module, "StructsWithMethodsInterface")
        ;
}

