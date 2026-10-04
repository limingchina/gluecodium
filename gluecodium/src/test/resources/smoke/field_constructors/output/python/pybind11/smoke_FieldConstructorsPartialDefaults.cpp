

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
#include "smoke/FieldConstructorsPartialDefaults.h"
#include "cstdint"
#include "string"

using FieldConstructorsPartialDefaults = ::smoke::FieldConstructorsPartialDefaults;



void register_smoke_FieldConstructorsPartialDefaults(py::module_& module) {
auto cls_FieldConstructorsPartialDefaults = py::class_<FieldConstructorsPartialDefaults>(module, "smoke_FieldConstructorsPartialDefaults")
        .def_property("string_field", [](const FieldConstructorsPartialDefaults& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](FieldConstructorsPartialDefaults& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def_property("int_field", [](const FieldConstructorsPartialDefaults& self) -> decltype(auto) {
            return
                (self.int_field)
            ;
        }, [](FieldConstructorsPartialDefaults& self, const int32_t value) {

                self.int_field = value;

        })
        .def_property("bool_field", [](const FieldConstructorsPartialDefaults& self) -> decltype(auto) {
            return
                (self.bool_field)
            ;
        }, [](FieldConstructorsPartialDefaults& self, const bool value) {

                self.bool_field = value;

        })
        .def(py::init<>())
        .def(py::init<int32_t, ::std::string>(), py::arg("int_field"), py::arg("string_field"))
        .def(py::init<bool, int32_t, ::std::string>(), py::arg("bool_field"), py::arg("int_field"), py::arg("string_field"))
        ;


}
