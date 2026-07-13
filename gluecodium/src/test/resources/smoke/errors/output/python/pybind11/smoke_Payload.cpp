

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/Payload.h"
#include "cstdint"
#include "string"

void register_Payload(py::module_& module) {
    py::class_<Payload>(module, "Payload")
        .def_readwrite("error_code", &Payload::error_code)
        .def_readwrite("message", &Payload::message)
        ;
}

