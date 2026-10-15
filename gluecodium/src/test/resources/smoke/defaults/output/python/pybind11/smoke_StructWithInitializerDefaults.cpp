

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
#include "smoke/DefaultValues.h"
#include "smoke/StructWithInitializerDefaults.h"
#include "cstdint"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

using StructWithInitializerDefaults = ::smoke::StructWithInitializerDefaults;



void register_smoke_StructWithInitializerDefaults(py::module_& module) {
auto cls_StructWithInitializerDefaults = py::class_<StructWithInitializerDefaults>(module, "smoke_StructWithInitializerDefaults")
        .def_property("ints_field", [](const StructWithInitializerDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.ints_field)
            );
        }, [](StructWithInitializerDefaults& self, const ::std::vector< int32_t >& value) {

                self.ints_field = value;

        })
        .def_property("floats_field", [](const StructWithInitializerDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.floats_field)
            );
        }, [](StructWithInitializerDefaults& self, const ::std::vector< float >& value) {

                self.floats_field = value;

        })
        .def_property("set_type_field", [](const StructWithInitializerDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.set_type_field)
            );
        }, [](StructWithInitializerDefaults& self, const ::std::unordered_set< ::std::string >& value) {

                self.set_type_field = value;

        })
        .def_property("map_field", [](const StructWithInitializerDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.map_field)
            );
        }, [](StructWithInitializerDefaults& self, const ::std::unordered_map< uint32_t, ::std::string >& value) {

                self.map_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::vector< int32_t >, ::std::vector< float >, ::std::unordered_set< ::std::string >, ::std::unordered_map< uint32_t, ::std::string >>(), py::arg("ints_field"), py::arg("floats_field"), py::arg("set_type_field"), py::arg("map_field"))
        ;


}
