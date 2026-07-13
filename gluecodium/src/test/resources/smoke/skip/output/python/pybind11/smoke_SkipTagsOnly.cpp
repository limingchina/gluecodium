

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkipTagsOnly.h"

void register_SkipTagsOnly(py::module_& module) {
    py::class_<SkipTagsOnly>(module, "SkipTagsOnly")
        ;
}

