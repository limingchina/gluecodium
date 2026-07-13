

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ImmutableStructWithDefaults.h"
#include "cstdint"

void register_ImmutableStructWithDefaults(py::module_& module) {
    py::class_<ImmutableStructWithDefaults>(module, "ImmutableStructWithDefaults")
        .def_readwrite("int_field", &ImmutableStructWithDefaults::int_field)
        ;
}

