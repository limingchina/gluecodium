

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ImmutableDefaultCtor.h"
#include "string"

void register_ImmutableDefaultCtor(py::module_& module) {
    py::class_<ImmutableDefaultCtor>(module, "ImmutableDefaultCtor")
        .def_readwrite("string_field", &ImmutableDefaultCtor::string_field)
        ;
}

