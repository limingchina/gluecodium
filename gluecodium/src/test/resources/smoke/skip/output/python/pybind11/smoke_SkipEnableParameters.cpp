

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkipEnableParameters.h"
#include "string"

void register_SkipEnableParameters(py::module_& module) {
    py::class_<SkipEnableParameters>(module, "SkipEnableParameters")
        .def("do_something", &SkipEnableParameters::do_something, py::arg("input"))
        ;
}

