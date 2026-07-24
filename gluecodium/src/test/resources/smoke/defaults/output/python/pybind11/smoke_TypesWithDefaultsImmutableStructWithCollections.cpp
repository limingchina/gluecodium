

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/TypesWithDefaults.h"
#include "cstdint"
#include "optional"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ImmutableStructWithCollections = ::smoke::TypesWithDefaults::ImmutableStructWithCollections;

void register_smoke_TypesWithDefaultsImmutableStructWithCollections(py::module_& module) {
    py::class_<ImmutableStructWithCollections>(module, "TypesWithDefaultsImmutableStructWithCollections")
        .def_readonly("nullable_list_field", &ImmutableStructWithCollections::nullable_list_field)
        .def_readonly("empty_list_field", &ImmutableStructWithCollections::empty_list_field)
        .def_readonly("values_list_field", &ImmutableStructWithCollections::values_list_field)
        .def_readonly("nullable_map_field", &ImmutableStructWithCollections::nullable_map_field)
        .def_readonly("empty_map_field", &ImmutableStructWithCollections::empty_map_field)
        .def_readonly("values_map_field", &ImmutableStructWithCollections::values_map_field)
        .def_readonly("nullable_set_field", &ImmutableStructWithCollections::nullable_set_field)
        .def_readonly("empty_set_field", &ImmutableStructWithCollections::empty_set_field)
        .def_readonly("values_set_field", &ImmutableStructWithCollections::values_set_field)
        .def(py::init<>())
        .def(py::init<std::optional< ::std::vector< int32_t > >, ::std::vector< int32_t >, ::std::vector< int32_t >, std::optional< ::std::unordered_map< int32_t, ::std::string > >, ::std::unordered_map< int32_t, ::std::string >, ::std::unordered_map< int32_t, ::std::string >, std::optional< ::std::unordered_set< ::std::string > >, ::std::unordered_set< ::std::string >, ::std::unordered_set< ::std::string >(), py::arg("nullable_list_field"), py::arg("empty_list_field"), py::arg("values_list_field"), py::arg("nullable_map_field"), py::arg("empty_map_field"), py::arg("values_map_field"), py::arg("nullable_set_field"), py::arg("empty_set_field"), py::arg("values_set_field"))
        ;
}

