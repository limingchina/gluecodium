

#include <Python.h>
#include <pybind11/pybind11.h>
#include "_opaque_types.h"
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
#include "smoke/EquatableStructWithInternalFields.h"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

using EquatableStructWithInternalFields = ::smoke::EquatableStructWithInternalFields;



void register_smoke_EquatableStructWithInternalFields(py::module_& module) {
auto cls_EquatableStructWithInternalFields = py::class_<EquatableStructWithInternalFields>(module, "smoke_EquatableStructWithInternalFields")
        .def_property("public_field", [](const EquatableStructWithInternalFields& self) -> decltype(auto) {
            return
                (self.public_field)
            ;
        }, [](EquatableStructWithInternalFields& self, const ::std::string& value) {

                self.public_field = value;

        })
        .def_property("_internal_field", [](const EquatableStructWithInternalFields& self) -> decltype(auto) {
            return
                (self.internal_field)
            ;
        }, [](EquatableStructWithInternalFields& self, const ::std::string& value) {

                self.internal_field = value;

        })
        .def_property("_internal_list_field", [](const EquatableStructWithInternalFields& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.internal_list_field)
            );
        }, [](EquatableStructWithInternalFields& self, const ::std::vector< ::std::string >& value) {

                self.internal_list_field = value;

        })
        .def_property("_internal_map_field", [](const EquatableStructWithInternalFields& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.internal_map_field)
            );
        }, [](EquatableStructWithInternalFields& self, const ::std::unordered_map< ::std::string, ::std::string >& value) {

                self.internal_map_field = value;

        })
        .def_property("_internal_set_field", [](const EquatableStructWithInternalFields& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.internal_set_field)
            );
        }, [](EquatableStructWithInternalFields& self, const ::std::unordered_set< ::std::string >& value) {

                self.internal_set_field = value;

        })
        .def(py::init<>())
        .def(py::init([](const ::std::string& public_field) {
            return EquatableStructWithInternalFields(public_field, ::std::string{}, ::std::vector< ::std::string >{}, ::std::unordered_map< ::std::string, ::std::string >{}, ::std::unordered_set< ::std::string >{});
        }), py::arg("public_field"))
        .def("__gluecodium_copy__", [](const EquatableStructWithInternalFields& self) { return EquatableStructWithInternalFields(self); })
        .def("__gluecodium_equals__", [](const EquatableStructWithInternalFields& lhs, const EquatableStructWithInternalFields& rhs) { return lhs == rhs; })
        .def("__gluecodium_hash__", [](const EquatableStructWithInternalFields& self) { return gluecodium::hash<EquatableStructWithInternalFields>{}(self); })
        ;


}
