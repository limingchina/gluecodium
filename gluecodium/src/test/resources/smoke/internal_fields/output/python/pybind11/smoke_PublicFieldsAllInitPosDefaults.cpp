

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
#include "smoke/PublicFieldsAllInitPosDefaults.h"
#include "string"

using PublicFieldsAllInitPosDefaults = ::smoke::PublicFieldsAllInitPosDefaults;



void register_smoke_PublicFieldsAllInitPosDefaults(py::module_& module) {
auto cls_PublicFieldsAllInitPosDefaults = py::class_<PublicFieldsAllInitPosDefaults>(module, "smoke_PublicFieldsAllInitPosDefaults")
        .def_property("public_field", [](const PublicFieldsAllInitPosDefaults& self) -> decltype(auto) {
            return
                (self.public_field)
            ;
        }, [](PublicFieldsAllInitPosDefaults& self, const ::std::string& value) {

                self.public_field = value;

        })
        .def_property("_internal_field", [](const PublicFieldsAllInitPosDefaults& self) -> decltype(auto) {
            return
                (self.internal_field)
            ;
        }, [](PublicFieldsAllInitPosDefaults& self, const ::std::string& value) {

                self.internal_field = value;

        })
        .def(py::init<>())
        .def(py::init([](const ::std::string& public_field) {
            return PublicFieldsAllInitPosDefaults(public_field, ::std::string{});
        }), py::arg("public_field"))
        ;


}
