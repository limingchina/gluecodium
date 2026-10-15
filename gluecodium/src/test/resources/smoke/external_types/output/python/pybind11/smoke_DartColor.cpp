

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
#include "smoke/DartColor.h"

using DartColor = ::smoke::DartColor;



void register_smoke_DartColor(py::module_& module) {
auto cls_DartColor = py::class_<DartColor>(module, "smoke_DartColor")
        .def_property("red", [](const DartColor& self) -> decltype(auto) {
            return
                (self.red)
            ;
        }, [](DartColor& self, const float value) {

                self.red = value;

        })
        .def_property("green", [](const DartColor& self) -> decltype(auto) {
            return
                (self.green)
            ;
        }, [](DartColor& self, const float value) {

                self.green = value;

        })
        .def_property("blue", [](const DartColor& self) -> decltype(auto) {
            return
                (self.blue)
            ;
        }, [](DartColor& self, const float value) {

                self.blue = value;

        })
        .def_property("alpha", [](const DartColor& self) -> decltype(auto) {
            return
                (self.alpha)
            ;
        }, [](DartColor& self, const float value) {

                self.alpha = value;

        })
        .def(py::init<>())
        .def(py::init<float, float, float>(), py::arg("red"), py::arg("green"), py::arg("blue"))
        .def(py::init<float, float, float, float>(), py::arg("red"), py::arg("green"), py::arg("blue"), py::arg("alpha"))
        .def("__gluecodium_copy__", [](const DartColor& self) { return DartColor(self); })
        .def("__gluecodium_equals__", [](const DartColor& lhs, const DartColor& rhs) { return lhs == rhs; })
        .def("__gluecodium_hash__", [](const DartColor& self) { return gluecodium::hash<DartColor>{}(self); })
        ;


}
