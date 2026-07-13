

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/TypeCollection.h"

void register_TypeCollection(py::module_& module) {
    py::class_<TypeCollection>(module, "TypeCollection")
        ;
}

