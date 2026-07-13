

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/OuterName.h"
#include "string"

void register_OuterName(py::module_& module) {
    py::class_<OuterName>(module, "OuterName")
        ;
}

