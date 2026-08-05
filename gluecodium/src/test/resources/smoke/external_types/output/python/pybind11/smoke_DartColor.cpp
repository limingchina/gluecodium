

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
#include "smoke/DartColor.h"

using DartColor = ::smoke::DartColor;



void register_smoke_DartColor(py::module_& module) {
auto cls_DartColor = py::class_<DartColor>(module, "smoke_DartColor")
        .def_readwrite("red", &DartColor::red)
        .def_readwrite("green", &DartColor::green)
        .def_readwrite("blue", &DartColor::blue)
        .def_readwrite("alpha", &DartColor::alpha)
        .def(py::init<>())
        .def(py::init<float, float, float>(), py::arg("red"), py::arg("green"), py::arg("blue"))
        .def(py::init<float, float, float, float>(), py::arg("red"), py::arg("green"), py::arg("blue"), py::arg("alpha"))
        .def("__eq__", [](const DartColor& lhs, const DartColor& rhs) { return lhs == rhs; })
        .def("__hash__", [](const DartColor& self) { return gluecodium::hash<DartColor>{}(self); })
        ;


}
