

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartPublicClass.h"

void register_DartPublicClass(py::module_& module) {
    py::class_<DartPublicClass>(module, "DartPublicClass")
        ;
}

