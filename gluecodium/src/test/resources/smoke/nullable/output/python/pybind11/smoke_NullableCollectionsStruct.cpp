

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/TimePointHash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/Nullable.h"
#include "smoke/NullableCollectionsStruct.h"
#include "chrono"
#include "cstdint"
#include "optional"
#include "unordered_map"
#include "vector"

void register_NullableCollectionsStruct(py::module_& module) {
    py::class_<NullableCollectionsStruct>(module, "NullableCollectionsStruct")
        .def_readwrite("dates", &NullableCollectionsStruct::dates)
        .def_readwrite("structs", &NullableCollectionsStruct::structs)
        ;
}

