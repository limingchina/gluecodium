

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/JavaInternalClassRev.h"

void register_JavaInternalClassRev(py::module_& module) {
    py::class_<JavaInternalClassRev>(module, "JavaInternalClassRev")
        ;
}

