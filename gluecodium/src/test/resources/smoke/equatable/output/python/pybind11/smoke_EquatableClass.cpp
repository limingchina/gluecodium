

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EquatableClass.h"
#include "smoke/PointerEquatableClass.h"
#include "cstdint"
#include "memory"
#include "string"

void register_EquatableClass(py::module_& module) {
    py::class_<EquatableClass>(module, "EquatableClass")
        ;
}

