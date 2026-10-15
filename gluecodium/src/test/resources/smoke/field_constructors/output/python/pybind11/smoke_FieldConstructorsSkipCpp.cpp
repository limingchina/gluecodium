

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
#include "smoke/FieldConstructorsSkipCpp.h"
#include "cstdint"
#include "string"

using FieldConstructorsSkipCpp = ::smoke::FieldConstructorsSkipCpp;



void register_smoke_FieldConstructorsSkipCpp(py::module_& module) {
auto cls_FieldConstructorsSkipCpp = py::class_<FieldConstructorsSkipCpp>(module, "smoke_FieldConstructorsSkipCpp")
        .def_property("string_field", [](const FieldConstructorsSkipCpp& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](FieldConstructorsSkipCpp& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def_property("int_field", [](const FieldConstructorsSkipCpp& self) -> decltype(auto) {
            return
                (self.int_field)
            ;
        }, [](FieldConstructorsSkipCpp& self, const int32_t value) {

                self.int_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::string, int32_t>(), py::arg("string_field"), py::arg("int_field"))
        ;


}
