

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
#include "smoke/PublicFieldsMixedInit.h"
#include "string"

using PublicFieldsMixedInit = ::smoke::PublicFieldsMixedInit;



void register_smoke_PublicFieldsMixedInit(py::module_& module) {
auto cls_PublicFieldsMixedInit = py::class_<PublicFieldsMixedInit>(module, "smoke_PublicFieldsMixedInit")
        .def_property("public_field1", [](const PublicFieldsMixedInit& self) -> decltype(auto) {
            return
                (self.public_field1)
            ;
        }, [](PublicFieldsMixedInit& self, const ::std::string& value) {

                self.public_field1 = value;

        })
        .def_property("public_field2", [](const PublicFieldsMixedInit& self) -> decltype(auto) {
            return
                (self.public_field2)
            ;
        }, [](PublicFieldsMixedInit& self, const ::std::string& value) {

                self.public_field2 = value;

        })
        .def_property("_internal_field", [](const PublicFieldsMixedInit& self) -> decltype(auto) {
            return
                (self.internal_field)
            ;
        }, [](PublicFieldsMixedInit& self, const ::std::string& value) {

                self.internal_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("public_field2"))
        .def(py::init([](const ::std::string& public_field1, const ::std::string& public_field2) {
            return PublicFieldsMixedInit(public_field1, public_field2, ::std::string{});
        }), py::arg("public_field1"), py::arg("public_field2"))
        ;


}
