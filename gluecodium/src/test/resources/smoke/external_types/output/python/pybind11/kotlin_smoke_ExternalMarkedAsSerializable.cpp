

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "kotlin_smoke/ExternalMarkedAsSerializable.h"
#include "cstdint"

void register_ExternalMarkedAsSerializable(py::module_& module) {
    py::class_<ExternalMarkedAsSerializable>(module, "ExternalMarkedAsSerializable")
        .def_readwrite("field", &ExternalMarkedAsSerializable::field)
        ;
}

