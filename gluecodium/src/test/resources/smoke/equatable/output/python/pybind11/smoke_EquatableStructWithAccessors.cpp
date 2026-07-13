

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EquatableStructWithAccessors.h"
#include "string"

void register_EquatableStructWithAccessors(py::module_& module) {
    py::class_<EquatableStructWithAccessors>(module, "EquatableStructWithAccessors")
        .def_readwrite("foo_field", &EquatableStructWithAccessors::foo_field)
        ;
}

