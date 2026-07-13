

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkipTypesTags.h"

void register_SkipTypesTags(py::module_& module) {
    py::class_<SkipTypesTags>(module, "SkipTypesTags")
        ;
}

