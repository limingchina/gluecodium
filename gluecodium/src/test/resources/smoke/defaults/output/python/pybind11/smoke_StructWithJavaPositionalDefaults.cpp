

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
#include "smoke/StructWithJavaPositionalDefaults.h"
#include "cstdint"
#include "string"

using StructWithJavaPositionalDefaults = ::smoke::StructWithJavaPositionalDefaults;



void register_smoke_StructWithJavaPositionalDefaults(py::module_& module) {
auto cls_StructWithJavaPositionalDefaults = py::class_<StructWithJavaPositionalDefaults>(module, "smoke_StructWithJavaPositionalDefaults")
        .def_property("first_init_field", [](const StructWithJavaPositionalDefaults& self) -> decltype(auto) {
            return
                (self.first_init_field)
            ;
        }, [](StructWithJavaPositionalDefaults& self, const int32_t value) {

                self.first_init_field = value;

        })
        .def_property("first_free_field", [](const StructWithJavaPositionalDefaults& self) -> decltype(auto) {
            return
                (self.first_free_field)
            ;
        }, [](StructWithJavaPositionalDefaults& self, const ::std::string& value) {

                self.first_free_field = value;

        })
        .def_property("second_init_field", [](const StructWithJavaPositionalDefaults& self) -> decltype(auto) {
            return
                (self.second_init_field)
            ;
        }, [](StructWithJavaPositionalDefaults& self, const float value) {

                self.second_init_field = value;

        })
        .def_property("second_free_field", [](const StructWithJavaPositionalDefaults& self) -> decltype(auto) {
            return
                (self.second_free_field)
            ;
        }, [](StructWithJavaPositionalDefaults& self, const bool value) {

                self.second_free_field = value;

        })
        .def_property("third_init_field", [](const StructWithJavaPositionalDefaults& self) -> decltype(auto) {
            return
                (self.third_init_field)
            ;
        }, [](StructWithJavaPositionalDefaults& self, const ::std::string& value) {

                self.third_init_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::string, bool>(), py::arg("first_free_field"), py::arg("second_free_field"))
        .def(py::init<int32_t, ::std::string, float, bool, ::std::string>(), py::arg("first_init_field"), py::arg("first_free_field"), py::arg("second_init_field"), py::arg("second_free_field"), py::arg("third_init_field"))
        ;


}
