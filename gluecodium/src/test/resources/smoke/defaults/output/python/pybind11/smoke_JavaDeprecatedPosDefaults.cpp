

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
#include "smoke/JavaDeprecatedPosDefaults.h"
#include "cstdint"
#include "string"

using JavaDeprecatedPosDefaults = ::smoke::JavaDeprecatedPosDefaults;



void register_smoke_JavaDeprecatedPosDefaults(py::module_& module) {
auto cls_JavaDeprecatedPosDefaults = py::class_<JavaDeprecatedPosDefaults>(module, "smoke_JavaDeprecatedPosDefaults")
        .def_property("first_init_field", [](const JavaDeprecatedPosDefaults& self) -> decltype(auto) {
            return
                (self.first_init_field)
            ;
        }, [](JavaDeprecatedPosDefaults& self, const int32_t value) {

                self.first_init_field = value;

        })
        .def_property("first_free_field", [](const JavaDeprecatedPosDefaults& self) -> decltype(auto) {
            return
                (self.first_free_field)
            ;
        }, [](JavaDeprecatedPosDefaults& self, const ::std::string& value) {

                self.first_free_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("first_free_field"))
        .def(py::init<int32_t, ::std::string>(), py::arg("first_init_field"), py::arg("first_free_field"))
        ;


}
