

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/IncludableClass.h"

void register_IncludableClass(py::module_& module) {
    py::class_<IncludableClass>(module, "IncludableClass")
        ;
}

