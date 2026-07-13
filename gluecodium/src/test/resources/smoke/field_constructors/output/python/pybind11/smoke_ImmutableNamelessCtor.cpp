

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ImmutableNamelessCtor.h"
#include "string"

void register_ImmutableNamelessCtor(py::module_& module) {
    py::class_<ImmutableNamelessCtor>(module, "ImmutableNamelessCtor")
        .def_readwrite("string_field", &ImmutableNamelessCtor::string_field)
        ;
}

