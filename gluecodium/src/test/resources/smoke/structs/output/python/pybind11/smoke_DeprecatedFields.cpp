

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
#include "smoke/DeprecatedFields.h"
#include "string"

using DeprecatedFields = ::smoke::DeprecatedFields;



void register_smoke_DeprecatedFields(py::module_& module) {
auto cls_DeprecatedFields = py::class_<DeprecatedFields>(module, "smoke_DeprecatedFields")
        .def_property("normal_field1", [](const DeprecatedFields& self) -> decltype(auto) {
            return
                (self.normal_field1)
            ;
        }, [](DeprecatedFields& self, const ::std::string& value) {

                self.normal_field1 = value;

        })
        .def_property("deprecated_field", [](const DeprecatedFields& self) -> decltype(auto) {
            return
                (self.deprecated_field)
            ;
        }, [](DeprecatedFields& self, const ::std::string& value) {

                self.deprecated_field = value;

        })
        .def_property("normal_field2", [](const DeprecatedFields& self) -> decltype(auto) {
            return
                (self.normal_field2)
            ;
        }, [](DeprecatedFields& self, const ::std::string& value) {

                self.normal_field2 = value;

        })
        .def(py::init<>())
        .def(py::init<::std::string, ::std::string>(), py::arg("normal_field1"), py::arg("normal_field2"))
        .def(py::init<::std::string, ::std::string, ::std::string>(), py::arg("normal_field1"), py::arg("deprecated_field"), py::arg("normal_field2"))
        ;


}
