

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ShouldNotInclude.h"
#include "string"

void register_ShouldNotInclude(py::module_& module) {
    py::class_<ShouldNotInclude>(module, "ShouldNotInclude")
        .def_readwrite("field", &ShouldNotInclude::field)
        ;
}

