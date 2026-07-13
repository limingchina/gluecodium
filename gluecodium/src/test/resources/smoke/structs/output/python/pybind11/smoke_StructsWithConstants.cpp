

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/RouteUtils.h"
#include "smoke/StructsWithConstants.h"
#include "string"

void register_StructsWithConstants(py::module_& module) {
    py::class_<StructsWithConstants>(module, "StructsWithConstants")
        ;
}

