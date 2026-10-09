

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
#include "smoke/FieldConstructorsWithLabels.h"
#include "cstdint"
#include "string"

using FieldConstructorsWithLabels = ::smoke::FieldConstructorsWithLabels;



void register_smoke_FieldConstructorsWithLabels(py::module_& module) {
auto cls_FieldConstructorsWithLabels = py::class_<FieldConstructorsWithLabels>(module, "smoke_FieldConstructorsWithLabels")
        .def_property("string_field", [](const FieldConstructorsWithLabels& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](FieldConstructorsWithLabels& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def_property("int_field", [](const FieldConstructorsWithLabels& self) -> decltype(auto) {
            return
                (self.int_field)
            ;
        }, [](FieldConstructorsWithLabels& self, const int32_t value) {

                self.int_field = value;

        })
        .def_property("bool_field", [](const FieldConstructorsWithLabels& self) -> decltype(auto) {
            return
                (self.bool_field)
            ;
        }, [](FieldConstructorsWithLabels& self, const bool value) {

                self.bool_field = value;

        })
        .def(py::init<>())
        .def(py::init<int32_t, bool>(), py::arg("int_field"), py::arg("bool_field"))
        .def(py::init<::std::string, int32_t, bool>(), py::arg("string_field"), py::arg("int_field"), py::arg("bool_field"))
        ;


}
