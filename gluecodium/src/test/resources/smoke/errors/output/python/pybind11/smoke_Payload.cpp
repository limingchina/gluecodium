

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
#include "smoke/Payload.h"
#include "cstdint"
#include "string"

using Payload = ::smoke::Payload;



void register_smoke_Payload(py::module_& module) {
auto cls_Payload = py::class_<Payload>(module, "smoke_Payload")
        .def_property("error_code", [](const Payload& self) -> decltype(auto) {
            return
                (self.error_code)
            ;
        }, [](Payload& self, const int32_t value) {

                self.error_code = value;

        })
        .def_property("message", [](const Payload& self) -> decltype(auto) {
            return
                (self.message)
            ;
        }, [](Payload& self, const ::std::string& value) {

                self.message = value;

        })
        .def(py::init<>())
        .def(py::init<int32_t, ::std::string>(), py::arg("error_code"), py::arg("message"))
        ;


}
