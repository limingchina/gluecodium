

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/StructWithNullableCollectionDefaults.h"
#include "optional"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructWithNullableCollectionDefaults = ::gluecodium::smoke::StructWithNullableCollectionDefaults;

void register_StructWithNullableCollectionDefaults(py::module_& module) {
    py::class_<StructWithNullableCollectionDefaults>(module, "StructWithNullableCollectionDefaults")
        .def_readwrite("nullable_list_field", &StructWithNullableCollectionDefaults::nullable_list_field)
        .def_readwrite("nullable_map_field", &StructWithNullableCollectionDefaults::nullable_map_field)
        .def_readwrite("nullable_set_field", &StructWithNullableCollectionDefaults::nullable_set_field)
        ;
}

