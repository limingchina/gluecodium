

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
#include "gluecodium/Hash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "smoke/EnumOptionSet.h"
#include "smoke/UseEnumOptionSet.h"
#include "unordered_set"

using UseEnumOptionSet = ::smoke::UseEnumOptionSet;



void register_smoke_UseEnumOptionSet(py::module_& module) {
auto cls_UseEnumOptionSet = py::class_<UseEnumOptionSet>(module, "smoke_UseEnumOptionSet")
        .def_property("set_field", [](const UseEnumOptionSet& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.set_field)
            );
        }, [](UseEnumOptionSet& self, const ::std::unordered_set< ::smoke::EnumOptionSet, ::gluecodium::hash< ::smoke::EnumOptionSet > >& value) {

                self.set_field = value;

        })
        .def_property("set_field_empty", [](const UseEnumOptionSet& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.set_field_empty)
            );
        }, [](UseEnumOptionSet& self, const ::std::unordered_set< ::smoke::EnumOptionSet, ::gluecodium::hash< ::smoke::EnumOptionSet > >& value) {

                self.set_field_empty = value;

        })
        .def_property("set_field_value", [](const UseEnumOptionSet& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.set_field_value)
            );
        }, [](UseEnumOptionSet& self, const ::std::unordered_set< ::smoke::EnumOptionSet, ::gluecodium::hash< ::smoke::EnumOptionSet > >& value) {

                self.set_field_value = value;

        })
        .def(py::init<>())
        .def(py::init<::std::unordered_set< ::smoke::EnumOptionSet, ::gluecodium::hash< ::smoke::EnumOptionSet > >>(), py::arg("set_field"))
        .def(py::init<::std::unordered_set< ::smoke::EnumOptionSet, ::gluecodium::hash< ::smoke::EnumOptionSet > >, ::std::unordered_set< ::smoke::EnumOptionSet, ::gluecodium::hash< ::smoke::EnumOptionSet > >, ::std::unordered_set< ::smoke::EnumOptionSet, ::gluecodium::hash< ::smoke::EnumOptionSet > >>(), py::arg("set_field"), py::arg("set_field_empty"), py::arg("set_field_value"))
                .def_static("round_trip", [](const ::std::unordered_set< ::smoke::EnumOptionSet, ::gluecodium::hash< ::smoke::EnumOptionSet > >& input) -> py::object {
                        return gluecodium::python::to_python_regular(gluecodium::python::call_native([&]() -> decltype(auto) { return UseEnumOptionSet::round_trip(input); }));
                }, py::arg("input"))
        ;


}
