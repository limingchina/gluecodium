

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/forward/Class1.h"

void register_Class1(py::module_& module) {
    py::class_<Class1>(module, "Class1")
        ;
}

