

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EnumsInTypeCollection.h"

void register_EnumsInTypeCollection(py::module_& module) {
    py::class_<EnumsInTypeCollection>(module, "EnumsInTypeCollection")
        ;
}

