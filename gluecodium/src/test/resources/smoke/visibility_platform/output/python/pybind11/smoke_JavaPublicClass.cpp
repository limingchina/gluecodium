

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/JavaPublicClass.h"

void register_JavaPublicClass(py::module_& module) {
    py::class_<JavaPublicClass>(module, "JavaPublicClass")
        ;
}

