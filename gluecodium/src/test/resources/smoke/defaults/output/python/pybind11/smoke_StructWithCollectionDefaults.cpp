

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
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/StructWithCollectionDefaults.h"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

using StructWithCollectionDefaults = ::smoke::StructWithCollectionDefaults;



void register_smoke_StructWithCollectionDefaults(py::module_& module) {
auto cls_StructWithCollectionDefaults = py::class_<StructWithCollectionDefaults>(module, "smoke_StructWithCollectionDefaults")
        .def_property("empty_list_field", [](const StructWithCollectionDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.empty_list_field)
            );
        }, [](StructWithCollectionDefaults& self, const ::std::vector< ::std::string >& value) {

                self.empty_list_field = value;

        })
        .def_property("empty_map_field", [](const StructWithCollectionDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.empty_map_field)
            );
        }, [](StructWithCollectionDefaults& self, const ::std::unordered_map< ::std::string, ::std::string >& value) {

                self.empty_map_field = value;

        })
        .def_property("empty_set_field", [](const StructWithCollectionDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.empty_set_field)
            );
        }, [](StructWithCollectionDefaults& self, const ::std::unordered_set< ::std::string >& value) {

                self.empty_set_field = value;

        })
        .def_property("list_field", [](const StructWithCollectionDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.list_field)
            );
        }, [](StructWithCollectionDefaults& self, const ::std::vector< ::std::string >& value) {

                self.list_field = value;

        })
        .def_property("map_field", [](const StructWithCollectionDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.map_field)
            );
        }, [](StructWithCollectionDefaults& self, const ::std::unordered_map< ::std::string, ::std::string >& value) {

                self.map_field = value;

        })
        .def_property("set_field", [](const StructWithCollectionDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.set_field)
            );
        }, [](StructWithCollectionDefaults& self, const ::std::unordered_set< ::std::string >& value) {

                self.set_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::vector< ::std::string >, ::std::unordered_map< ::std::string, ::std::string >, ::std::unordered_set< ::std::string >, ::std::vector< ::std::string >, ::std::unordered_map< ::std::string, ::std::string >, ::std::unordered_set< ::std::string >>(), py::arg("empty_list_field"), py::arg("empty_map_field"), py::arg("empty_set_field"), py::arg("list_field"), py::arg("map_field"), py::arg("set_field"))
        ;


}
