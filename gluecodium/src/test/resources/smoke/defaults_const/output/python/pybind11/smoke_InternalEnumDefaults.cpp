

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
#include "gluecodium/VectorHash.h"
#include "smoke/FooBarEnum.h"
#include "smoke/InternalEnumDefaults.h"
#include "vector"

using InternalEnumDefaults = ::smoke::InternalEnumDefaults;



void register_smoke_InternalEnumDefaults(py::module_& module) {
auto cls_InternalEnumDefaults = py::class_<InternalEnumDefaults>(module, "smoke_InternalEnumDefaults")
        .def_property("public_field", [](const InternalEnumDefaults& self) -> decltype(auto) {
            return
                (self.public_field)
            ;
        }, [](InternalEnumDefaults& self, const ::smoke::FooBarEnum value) {

                self.public_field = value;

        })
        .def_property("public_list_field", [](const InternalEnumDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.public_list_field)
            );
        }, [](InternalEnumDefaults& self, const ::std::vector< ::smoke::FooBarEnum >& value) {

                self.public_list_field = value;

        })
        .def_property("_internal_field", [](const InternalEnumDefaults& self) -> decltype(auto) {
            return
                (self.internal_field)
            ;
        }, [](InternalEnumDefaults& self, const ::smoke::FooBarEnum value) {

                self.internal_field = value;

        })
        .def_property("_internal_list_field", [](const InternalEnumDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.internal_list_field)
            );
        }, [](InternalEnumDefaults& self, const ::std::vector< ::smoke::FooBarEnum >& value) {

                self.internal_list_field = value;

        })
        .def(py::init<>())
        .def(py::init([](const ::smoke::FooBarEnum& public_field, const ::std::vector< ::smoke::FooBarEnum >& public_list_field) {
            return InternalEnumDefaults(public_field, public_list_field, ::smoke::FooBarEnum{}, ::std::vector< ::smoke::FooBarEnum >{});
        }), py::arg("public_field"), py::arg("public_list_field"))
        ;


}
