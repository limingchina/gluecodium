

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
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

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using NullableCollectionsStruct = ::gluecodium::smoke::NullableCollectionsStruct;

void register_NullableCollectionsStruct(py::module_& module) {
    py::class_<NullableCollectionsStruct>(module, "NullableCollectionsStruct")
        .def_readwrite("dates", &NullableCollectionsStruct::dates)
        .def_readwrite("structs", &NullableCollectionsStruct::structs)
        ;
}

