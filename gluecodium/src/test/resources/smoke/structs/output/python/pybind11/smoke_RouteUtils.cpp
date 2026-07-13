

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/RouteUtils.h"

void register_RouteUtils(py::module_& module) {
    py::class_<RouteUtils>(module, "RouteUtils")
        ;
}

