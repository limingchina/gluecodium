

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/JavaSwiftInternalClass.h"

void register_JavaSwiftInternalClass(py::module_& module) {
    py::class_<JavaSwiftInternalClass>(module, "JavaSwiftInternalClass")
        ;
}

