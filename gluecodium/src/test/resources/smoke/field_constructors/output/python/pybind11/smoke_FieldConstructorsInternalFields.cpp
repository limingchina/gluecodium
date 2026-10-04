

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
#include "smoke/FieldConstructorsInternalFields.h"
#include "cstdint"
#include "string"

using FieldConstructorsInternalFields = ::smoke::FieldConstructorsInternalFields;



void register_smoke_FieldConstructorsInternalFields(py::module_& module) {
auto cls_FieldConstructorsInternalFields = py::class_<FieldConstructorsInternalFields>(module, "smoke_FieldConstructorsInternalFields")
        .def_property("string_field", [](const FieldConstructorsInternalFields& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](FieldConstructorsInternalFields& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def_property("int_field", [](const FieldConstructorsInternalFields& self) -> decltype(auto) {
            return
                (self.int_field)
            ;
        }, [](FieldConstructorsInternalFields& self, const int32_t value) {

                self.int_field = value;

        })
        .def_property("_bool_field", [](const FieldConstructorsInternalFields& self) -> decltype(auto) {
            return
                (self.bool_field)
            ;
        }, [](FieldConstructorsInternalFields& self, const bool value) {

                self.bool_field = value;

        })
        .def(py::init<>())
        .def(py::init<int32_t, ::std::string>(), py::arg("int_field"), py::arg("string_field"))
        .def(py::init<bool, int32_t, ::std::string>(), py::arg("_bool_field"), py::arg("int_field"), py::arg("string_field"))
        ;


}
