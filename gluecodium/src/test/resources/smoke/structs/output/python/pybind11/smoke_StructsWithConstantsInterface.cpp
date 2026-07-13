

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/RouteUtils.h"
#include "smoke/StructsWithConstantsInterface.h"
#include "string"
#include "vector"

void register_StructsWithConstantsInterface(py::module_& module) {
    py::class_<StructsWithConstantsInterface>(module, "StructsWithConstantsInterface")
        ;
}

