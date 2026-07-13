

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/JavaInternalClass.h"

void register_JavaInternalClass(py::module_& module) {
    py::class_<JavaInternalClass>(module, "JavaInternalClass")
        ;
}

