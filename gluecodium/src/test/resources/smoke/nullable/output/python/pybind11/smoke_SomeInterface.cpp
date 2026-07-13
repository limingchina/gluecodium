

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SomeInterface.h"

void register_SomeInterface(py::module_& module) {
    py::class_<SomeInterface>(module, "SomeInterface")
        ;
}

