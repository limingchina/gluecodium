

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/InternalChild.h"

void register_InternalChild(py::module_& module) {
    py::class_<InternalChild>(module, "InternalChild")
        ;
}

