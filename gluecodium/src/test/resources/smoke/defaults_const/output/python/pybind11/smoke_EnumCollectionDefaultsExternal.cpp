

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

using EnumCollectionDefaultsExternal = ::smoke::EnumCollectionDefaultsExternal;



void register_smoke_EnumCollectionDefaultsExternal(py::module_& module) {
auto cls_EnumCollectionDefaultsExternal = py::class_<EnumCollectionDefaultsExternal>(module, "smoke_EnumCollectionDefaultsExternal")
        .def_readwrite("list_field", &EnumCollectionDefaultsExternal::list_field)
        .def_readwrite("set_field", &EnumCollectionDefaultsExternal::set_field)
        .def_readwrite("map_field", &EnumCollectionDefaultsExternal::map_field)
        .def(py::init<>())
        .def(py::init<::std::vector< foo::AlienEnum1 >, ::std::unordered_set< foo::AlienEnum2, ::gluecodium::hash< foo::AlienEnum2 > >, ::std::unordered_map< foo::AlienEnum3, foo::AlienEnum4, ::gluecodium::hash< foo::AlienEnum3 > >>(), py::arg("list_field"), py::arg("set_field"), py::arg("map_field"))
        ;


}
