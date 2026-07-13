

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "foo/AlienEnum1.h"
#include "foo/AlienEnum2.h"
#include "foo/AlienEnum3.h"
#include "foo/AlienEnum4.h"
#include "gluecodium/Hash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/EnumCollectionDefaultsExternal.h"
#include "unordered_map"
#include "unordered_set"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EnumCollectionDefaultsExternal = ::gluecodium::smoke::EnumCollectionDefaultsExternal;

void register_EnumCollectionDefaultsExternal(py::module_& module) {
    py::class_<EnumCollectionDefaultsExternal>(module, "EnumCollectionDefaultsExternal")
        .def_readwrite("list_field", &EnumCollectionDefaultsExternal::list_field)
        .def_readwrite("set_field", &EnumCollectionDefaultsExternal::set_field)
        .def_readwrite("map_field", &EnumCollectionDefaultsExternal::map_field)
        ;
}

