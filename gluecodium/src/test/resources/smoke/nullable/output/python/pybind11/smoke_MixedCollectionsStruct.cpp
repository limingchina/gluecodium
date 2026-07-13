

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/TimePointHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/MixedCollectionsStruct.h"
#include "chrono"
#include "optional"
#include "vector"

void register_MixedCollectionsStruct(py::module_& module) {
    py::class_<MixedCollectionsStruct>(module, "MixedCollectionsStruct")
        .def_readwrite("almost_dates", &MixedCollectionsStruct::almost_dates)
        .def_readwrite("dates", &MixedCollectionsStruct::dates)
        ;
}

