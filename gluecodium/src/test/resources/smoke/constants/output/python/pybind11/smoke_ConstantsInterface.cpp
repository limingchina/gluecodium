

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ConstantsInterface.h"

void register_ConstantsInterface(py::module_& module) {
    py::class_<ConstantsInterface>(module, "ConstantsInterface")
        ;
}

