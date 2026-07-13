

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "fire/Enum1.h"
#include "fire/Enum2.h"
#include "fire/Enum3.h"
#include "fire/Enum4.h"
#include "gluecodium/Hash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/EnumCollectionDefaults.h"
#include "unordered_map"
#include "unordered_set"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EnumCollectionDefaults = ::gluecodium::smoke::EnumCollectionDefaults;

void register_EnumCollectionDefaults(py::module_& module) {
    py::class_<EnumCollectionDefaults>(module, "EnumCollectionDefaults")
        .def_readwrite("list_field", &EnumCollectionDefaults::list_field)
        .def_readwrite("set_field", &EnumCollectionDefaults::set_field)
        .def_readwrite("map_field", &EnumCollectionDefaults::map_field)
        .def(py::init<>())
        .def(py::init<::std::vector< ::fire::Enum1 >, ::std::unordered_set< ::fire::Enum2, ::gluecodium::hash< ::fire::Enum2 > >, ::std::unordered_map< ::fire::Enum3, ::fire::Enum4, ::gluecodium::hash< ::fire::Enum3 > >>(), py::arg("list_field"), py::arg("set_field"), py::arg("map_field"))
        ;
}

