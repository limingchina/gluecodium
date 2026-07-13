

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/KotlinPublicClass.h"

void register_KotlinPublicClass(py::module_& module) {
    py::class_<KotlinPublicClass>(module, "KotlinPublicClass")
        ;
}

