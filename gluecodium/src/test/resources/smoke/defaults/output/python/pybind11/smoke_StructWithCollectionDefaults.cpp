

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
#include "smoke/StructWithCollectionDefaults.h"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructWithCollectionDefaults = ::smoke::StructWithCollectionDefaults;

void register_smoke_StructWithCollectionDefaults(py::module_& module) {
    py::class_<StructWithCollectionDefaults>(module, "smoke_StructWithCollectionDefaults")
        .def_readwrite("empty_list_field", &StructWithCollectionDefaults::empty_list_field)
        .def_readwrite("empty_map_field", &StructWithCollectionDefaults::empty_map_field)
        .def_readwrite("empty_set_field", &StructWithCollectionDefaults::empty_set_field)
        .def_readwrite("list_field", &StructWithCollectionDefaults::list_field)
        .def_readwrite("map_field", &StructWithCollectionDefaults::map_field)
        .def_readwrite("set_field", &StructWithCollectionDefaults::set_field)
        .def(py::init<>())
        .def(py::init<::std::vector< ::std::string >, ::std::unordered_map< ::std::string, ::std::string >, ::std::unordered_set< ::std::string >, ::std::vector< ::std::string >, ::std::unordered_map< ::std::string, ::std::string >, ::std::unordered_set< ::std::string >>(), py::arg("empty_list_field"), py::arg("empty_map_field"), py::arg("empty_set_field"), py::arg("list_field"), py::arg("map_field"), py::arg("set_field"))
        ;
}

