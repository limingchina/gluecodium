

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/UnusedTopLevelPoint.h"
#include "string"

void register_UnusedTopLevelPoint(py::module_& module) {
    py::class_<UnusedTopLevelPoint>(module, "UnusedTopLevelPoint")
        .def_readwrite("foo", &UnusedTopLevelPoint::foo)
        ;
}

