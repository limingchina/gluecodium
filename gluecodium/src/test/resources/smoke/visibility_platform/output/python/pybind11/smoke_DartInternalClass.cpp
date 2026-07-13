

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartInternalClass.h"

void register_DartInternalClass(py::module_& module) {
    py::class_<DartInternalClass>(module, "DartInternalClass")
        ;
}

