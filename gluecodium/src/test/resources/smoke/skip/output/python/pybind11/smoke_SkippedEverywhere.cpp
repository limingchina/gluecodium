

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/UnorderedMapHash.h"
#include "smoke/SkipTypes.h"
#include "smoke/SkippedEverywhere.h"
#include "cstdint"
#include "string"
#include "unordered_map"

void register_SkippedEverywhere(py::module_& module) {
    py::class_<SkippedEverywhere>(module, "SkippedEverywhere")
        .def_readwrite("nothing_to_see_here", &SkippedEverywhere::nothing_to_see_here)
        .def("use_map_in_dart", &SkippedEverywhere::use_map_in_dart, py::arg("foo"))
        ;
}

