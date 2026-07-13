

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/MyOuterClass.h"

void register_MyOuterClass(py::module_& module) {
    py::class_<MyOuterClass>(module, "MyOuterClass")
        ;
}

