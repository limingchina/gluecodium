

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/PublicTypeCollection.h"

void register_PublicTypeCollection(py::module_& module) {
    py::class_<PublicTypeCollection>(module, "PublicTypeCollection")
        ;
}

