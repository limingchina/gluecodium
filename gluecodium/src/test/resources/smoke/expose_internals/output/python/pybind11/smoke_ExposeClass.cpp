

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ExposeClass.h"

void register_ExposeClass(py::module_& module) {
    py::class_<ExposeClass>(module, "ExposeClass")
        ;
}

