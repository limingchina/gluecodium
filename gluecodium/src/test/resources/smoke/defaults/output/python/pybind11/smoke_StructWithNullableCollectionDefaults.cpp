

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
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/StructWithNullableCollectionDefaults.h"
#include "optional"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

using StructWithNullableCollectionDefaults = ::smoke::StructWithNullableCollectionDefaults;



void register_smoke_StructWithNullableCollectionDefaults(py::module_& module) {
auto cls_StructWithNullableCollectionDefaults = py::class_<StructWithNullableCollectionDefaults>(module, "smoke_StructWithNullableCollectionDefaults")
        .def_readwrite("nullable_list_field", &StructWithNullableCollectionDefaults::nullable_list_field)
        .def_readwrite("nullable_map_field", &StructWithNullableCollectionDefaults::nullable_map_field)
        .def_readwrite("nullable_set_field", &StructWithNullableCollectionDefaults::nullable_set_field)
        .def(py::init<>())
        .def(py::init<std::optional< ::std::vector< ::std::string > >, std::optional< ::std::unordered_map< ::std::string, ::std::string > >, std::optional< ::std::unordered_set< ::std::string > >>(), py::arg("nullable_list_field"), py::arg("nullable_map_field"), py::arg("nullable_set_field"))
        ;


}
