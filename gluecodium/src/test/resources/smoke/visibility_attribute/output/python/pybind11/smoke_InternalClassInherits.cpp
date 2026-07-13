

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/InternalClassInherits.h"
#include "string"

void register_InternalClassInherits(py::module_& module) {
    py::class_<InternalClassInherits>(module, "InternalClassInherits")
        ;
}

