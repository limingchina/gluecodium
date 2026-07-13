

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ExternalClass.h"
#include "cstdint"
#include "memory"

void register_ExternalClass(py::module_& module) {
    py::class_<ExternalClass>(module, "ExternalClass")
        .def("create", &ExternalClass::create)
        ;
}

