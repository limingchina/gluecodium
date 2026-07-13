

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SwiftInternalClass.h"

void register_SwiftInternalClass(py::module_& module) {
    py::class_<SwiftInternalClass>(module, "SwiftInternalClass")
        ;
}

