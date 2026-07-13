

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/StructWithNullableCollectionDefaults.h"
#include "optional"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

void register_StructWithNullableCollectionDefaults(py::module_& module) {
    py::class_<StructWithNullableCollectionDefaults>(module, "StructWithNullableCollectionDefaults")
        .def_readwrite("nullable_list_field", &StructWithNullableCollectionDefaults::nullable_list_field)
        .def_readwrite("nullable_map_field", &StructWithNullableCollectionDefaults::nullable_map_field)
        .def_readwrite("nullable_set_field", &StructWithNullableCollectionDefaults::nullable_set_field)
        ;
}

