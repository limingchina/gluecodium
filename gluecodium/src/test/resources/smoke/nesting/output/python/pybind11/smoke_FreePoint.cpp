

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
#include "smoke/FreePoint.h"

using FreePoint = ::smoke::FreePoint;



void register_smoke_FreePoint(py::module_& module) {
auto cls_FreePoint = py::class_<FreePoint>(module, "smoke_FreePoint")
        .def_property("x", [](const FreePoint& self) -> decltype(auto) {
            return
                (self.x)
            ;
        }, [](FreePoint& self, const double value) {

                self.x = value;

        })
        .def_property("y", [](const FreePoint& self) -> decltype(auto) {
            return
                (self.y)
            ;
        }, [](FreePoint& self, const double value) {

                self.y = value;

        })
        .def(py::init<>())
        .def(py::init<double, double>(), py::arg("x"), py::arg("y"))
        .def("flip", &FreePoint::flip, py::call_guard<py::gil_scoped_release>())
        ;


}
