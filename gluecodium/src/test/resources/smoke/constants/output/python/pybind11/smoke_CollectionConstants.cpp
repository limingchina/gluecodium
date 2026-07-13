

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/CollectionConstants.h"

void register_CollectionConstants(py::module_& module) {
    py::class_<CollectionConstants>(module, "CollectionConstants")
        ;
}

