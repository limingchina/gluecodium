

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
#include "gluecodium/TimePointHash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/Nullable.h"
#include "smoke/NullableCollectionsStruct.h"
#include "chrono"
#include "cstdint"
#include "unordered_map"
#include "vector"

using NullableCollectionsStruct = ::smoke::NullableCollectionsStruct;



void register_smoke_NullableCollectionsStruct(py::module_& module) {
auto cls_NullableCollectionsStruct = py::class_<NullableCollectionsStruct>(module, "smoke_NullableCollectionsStruct")
        .def_property("dates", [](const NullableCollectionsStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.dates)
            );
        }, [](NullableCollectionsStruct& self, const ::std::vector< ::gluecodium::optional< ::std::chrono::system_clock::time_point > >& value) {

                self.dates = value;

        })
        .def_property("structs", [](const NullableCollectionsStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.structs)
            );
        }, [](NullableCollectionsStruct& self, const ::std::unordered_map< int32_t, ::gluecodium::optional< ::smoke::Nullable::SomeStruct > >& value) {

                self.structs = value;

        })
        .def(py::init<>())
        .def(py::init<::std::vector< ::gluecodium::optional< ::std::chrono::system_clock::time_point > >, ::std::unordered_map< int32_t, ::gluecodium::optional< ::smoke::Nullable::SomeStruct > >>(), py::arg("dates"), py::arg("structs"))
        ;


}
