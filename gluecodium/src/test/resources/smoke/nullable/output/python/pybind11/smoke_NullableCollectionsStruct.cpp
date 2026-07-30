

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

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
using NullableCollectionsStruct = ::smoke::NullableCollectionsStruct;

void register_smoke_NullableCollectionsStruct(py::module_& module) {
    py::class_<NullableCollectionsStruct>(module, "smoke_NullableCollectionsStruct")
        .def_readwrite("dates", &NullableCollectionsStruct::dates)
        .def_readwrite("structs", &NullableCollectionsStruct::structs)
        .def(py::init<>())
        .def(py::init<::std::vector< std::optional< ::std::chrono::system_clock::time_point > >, ::std::unordered_map< int32_t, std::optional< ::smoke::Nullable::SomeStruct > >>(), py::arg("dates"), py::arg("structs"))
        ;
}

