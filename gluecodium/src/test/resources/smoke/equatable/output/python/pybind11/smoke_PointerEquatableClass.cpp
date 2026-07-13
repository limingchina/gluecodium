

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/PointerEquatableClass.h"

void register_PointerEquatableClass(py::module_& module) {
    py::class_<PointerEquatableClass>(module, "PointerEquatableClass")
        ;
}

