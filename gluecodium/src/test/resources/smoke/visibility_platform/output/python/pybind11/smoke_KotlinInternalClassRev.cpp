

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/KotlinInternalClassRev.h"

void register_KotlinInternalClassRev(py::module_& module) {
    py::class_<KotlinInternalClassRev>(module, "KotlinInternalClassRev")
        ;
}

