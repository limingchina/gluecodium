

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SwiftInternalClassRev.h"

void register_SwiftInternalClassRev(py::module_& module) {
    py::class_<SwiftInternalClassRev>(module, "SwiftInternalClassRev")
        ;
}

