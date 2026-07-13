

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ConstantsSkipCpp.h"

void register_ConstantsSkipCpp(py::module_& module) {
    py::class_<ConstantsSkipCpp>(module, "ConstantsSkipCpp")
        ;
}

