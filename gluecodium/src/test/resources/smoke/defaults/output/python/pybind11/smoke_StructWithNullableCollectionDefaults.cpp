

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
#include "gluecodium/Optional.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/StructWithNullableCollectionDefaults.h"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

using StructWithNullableCollectionDefaults = ::smoke::StructWithNullableCollectionDefaults;



void register_smoke_StructWithNullableCollectionDefaults(py::module_& module) {
auto cls_StructWithNullableCollectionDefaults = py::class_<StructWithNullableCollectionDefaults>(module, "smoke_StructWithNullableCollectionDefaults")
        .def_property("nullable_list_field", [](const StructWithNullableCollectionDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.nullable_list_field)
            );
        }, [](StructWithNullableCollectionDefaults& self, const ::gluecodium::optional< ::std::vector< ::std::string > >& value) {

                self.nullable_list_field = value;

        })
        .def_property("nullable_map_field", [](const StructWithNullableCollectionDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.nullable_map_field)
            );
        }, [](StructWithNullableCollectionDefaults& self, const ::gluecodium::optional< ::std::unordered_map< ::std::string, ::std::string > >& value) {

                self.nullable_map_field = value;

        })
        .def_property("nullable_set_field", [](const StructWithNullableCollectionDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.nullable_set_field)
            );
        }, [](StructWithNullableCollectionDefaults& self, const ::gluecodium::optional< ::std::unordered_set< ::std::string > >& value) {

                self.nullable_set_field = value;

        })
        .def(py::init<>())
        .def(py::init<::gluecodium::optional< ::std::vector< ::std::string > >, ::gluecodium::optional< ::std::unordered_map< ::std::string, ::std::string > >, ::gluecodium::optional< ::std::unordered_set< ::std::string > >>(), py::arg("nullable_list_field"), py::arg("nullable_map_field"), py::arg("nullable_set_field"))
        ;


}
