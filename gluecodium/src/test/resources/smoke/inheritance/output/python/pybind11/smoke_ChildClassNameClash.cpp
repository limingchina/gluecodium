

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ChildClassNameClash.h"
#include "string"

void register_ChildClassNameClash(py::module_& module) {
    py::class_<ChildClassNameClash>(module, "ChildClassNameClash")
        ;
}

