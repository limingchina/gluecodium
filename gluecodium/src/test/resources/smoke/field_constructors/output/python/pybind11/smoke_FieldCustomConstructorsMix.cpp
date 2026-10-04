

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
#include "smoke/FieldCustomConstructorsMix.h"
#include "cstdint"
#include "string"

using FieldCustomConstructorsMix = ::smoke::FieldCustomConstructorsMix;



void register_smoke_FieldCustomConstructorsMix(py::module_& module) {
auto cls_FieldCustomConstructorsMix = py::class_<FieldCustomConstructorsMix>(module, "smoke_FieldCustomConstructorsMix")
        .def_property("string_field", [](const FieldCustomConstructorsMix& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](FieldCustomConstructorsMix& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def_property("int_field", [](const FieldCustomConstructorsMix& self) -> decltype(auto) {
            return
                (self.int_field)
            ;
        }, [](FieldCustomConstructorsMix& self, const int32_t value) {

                self.int_field = value;

        })
        .def_property("bool_field", [](const FieldCustomConstructorsMix& self) -> decltype(auto) {
            return
                (self.bool_field)
            ;
        }, [](FieldCustomConstructorsMix& self, const bool value) {

                self.bool_field = value;

        })
        .def(py::init<>())
        .def(py::init<int32_t>(), py::arg("int_field"))
        .def_static("create_me", &FieldCustomConstructorsMix::create_me, py::arg("int_value"), py::arg("dummy"), py::call_guard<py::gil_scoped_release>())
        ;


}
