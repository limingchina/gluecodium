

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
#include "smoke/StructWithAllDefaults.h"
#include "cstdint"
#include "string"

using StructWithAllDefaults = ::smoke::StructWithAllDefaults;



void register_smoke_StructWithAllDefaults(py::module_& module) {
auto cls_StructWithAllDefaults = py::class_<StructWithAllDefaults>(module, "smoke_StructWithAllDefaults")
        .def_property("int_field", [](const StructWithAllDefaults& self) -> decltype(auto) {
            return
                (self.int_field)
            ;
        }, [](StructWithAllDefaults& self, const int32_t value) {

                self.int_field = value;

        })
        .def_property("string_field", [](const StructWithAllDefaults& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](StructWithAllDefaults& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def(py::init<>())
        .def(py::init<int32_t, ::std::string>(), py::arg("int_field"), py::arg("string_field"))
        ;


}
