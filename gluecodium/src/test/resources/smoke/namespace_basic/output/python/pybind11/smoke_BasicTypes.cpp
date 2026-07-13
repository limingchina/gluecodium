

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "root/space/smoke/BasicTypes.h"
#include "string"

void register_BasicTypes(py::module_& module) {
    py::class_<BasicTypes>(module, "BasicTypes")
        ;
}

