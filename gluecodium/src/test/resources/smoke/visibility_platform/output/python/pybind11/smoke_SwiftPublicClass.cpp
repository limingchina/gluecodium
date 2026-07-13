

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SwiftPublicClass.h"

void register_SwiftPublicClass(py::module_& module) {
    py::class_<SwiftPublicClass>(module, "SwiftPublicClass")
        ;
}

