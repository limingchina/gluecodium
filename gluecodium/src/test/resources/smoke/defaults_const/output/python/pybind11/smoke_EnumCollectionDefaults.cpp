

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

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

using EnumCollectionDefaults = ::smoke::EnumCollectionDefaults;



void register_smoke_EnumCollectionDefaults(py::module_& module) {
auto cls_EnumCollectionDefaults = py::class_<EnumCollectionDefaults>(module, "smoke_EnumCollectionDefaults")
        .def_property("list_field", [](const EnumCollectionDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.list_field)
            );
        }, [](EnumCollectionDefaults& self, const ::std::vector< ::fire::Enum1 >& value) {

                self.list_field = value;

        })
        .def_property("set_field", [](const EnumCollectionDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.set_field)
            );
        }, [](EnumCollectionDefaults& self, const ::std::unordered_set< ::fire::Enum2, ::gluecodium::hash< ::fire::Enum2 > >& value) {

                self.set_field = value;

        })
        .def_property("map_field", [](const EnumCollectionDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.map_field)
            );
        }, [](EnumCollectionDefaults& self, const ::std::unordered_map< ::fire::Enum3, ::fire::Enum4, ::gluecodium::hash< ::fire::Enum3 > >& value) {

                self.map_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::vector< ::fire::Enum1 >, ::std::unordered_set< ::fire::Enum2, ::gluecodium::hash< ::fire::Enum2 > >, ::std::unordered_map< ::fire::Enum3, ::fire::Enum4, ::gluecodium::hash< ::fire::Enum3 > >>(), py::arg("list_field"), py::arg("set_field"), py::arg("map_field"))
        ;


}
