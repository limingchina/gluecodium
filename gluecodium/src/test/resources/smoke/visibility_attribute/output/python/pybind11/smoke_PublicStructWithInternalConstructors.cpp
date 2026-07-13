

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/PublicStructWithInternalConstructors.h"
#include "cstdint"

void register_PublicStructWithInternalConstructors(py::module_& module) {
    py::class_<PublicStructWithInternalConstructors>(module, "PublicStructWithInternalConstructors")
        .def_readwrite("some_var", &PublicStructWithInternalConstructors::some_var)
        .def("make", &PublicStructWithInternalConstructors::make)
        ;
}

