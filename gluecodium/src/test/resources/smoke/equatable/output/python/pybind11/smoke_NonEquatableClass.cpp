

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/NonEquatableClass.h"

void register_NonEquatableClass(py::module_& module) {
    py::class_<NonEquatableClass>(module, "NonEquatableClass")
        ;
}

