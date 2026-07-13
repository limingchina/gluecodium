

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartInternalClassRev.h"

void register_DartInternalClassRev(py::module_& module) {
    py::class_<DartInternalClassRev>(module, "DartInternalClassRev")
        ;
}

