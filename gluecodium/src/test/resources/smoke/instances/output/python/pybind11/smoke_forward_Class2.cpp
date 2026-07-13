

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/forward/Class2.h"

void register_Class2(py::module_& module) {
    py::class_<Class2>(module, "Class2")
        ;
}

