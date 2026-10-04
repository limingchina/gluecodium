

#include <Python.h>
#include <pybind11/pybind11.h>
#include "_opaque_types.h"
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "kotlin_smoke/SystemColor.h"

using SystemColor = ::kotlin_smoke::SystemColor;



void register_kotlin_smoke_SystemColor(py::module_& module) {
auto cls_SystemColor = py::class_<SystemColor>(module, "kotlin_smoke_SystemColor")
        .def_property("red", [](const SystemColor& self) -> decltype(auto) {
            return
                (self.red)
            ;
        }, [](SystemColor& self, const float value) {

                self.red = value;

        })
        .def_property("green", [](const SystemColor& self) -> decltype(auto) {
            return
                (self.green)
            ;
        }, [](SystemColor& self, const float value) {

                self.green = value;

        })
        .def_property("blue", [](const SystemColor& self) -> decltype(auto) {
            return
                (self.blue)
            ;
        }, [](SystemColor& self, const float value) {

                self.blue = value;

        })
        .def_property("alpha", [](const SystemColor& self) -> decltype(auto) {
            return
                (self.alpha)
            ;
        }, [](SystemColor& self, const float value) {

                self.alpha = value;

        })
        .def(py::init<>())
        .def(py::init<float, float, float, float>(), py::arg("red"), py::arg("green"), py::arg("blue"), py::arg("alpha"))
        ;


}
