

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "include/ExternalTypeInTypesCollection.h"
#include "smoke/ExternalTypeInTypesCollection.h"
#include "cstdint"

void register_ExternalTypeInTypesCollection(py::module_& module) {
    py::class_<ExternalTypeInTypesCollection>(module, "ExternalTypeInTypesCollection")
        ;
}

