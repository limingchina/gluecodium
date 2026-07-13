

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "foo/Bar.h"
#include "smoke/ExternalEquatable.h"
#include "string"

void register_ExternalEquatable(py::module_& module) {
    py::class_<ExternalEquatable>(module, "ExternalEquatable")
        ;
}

