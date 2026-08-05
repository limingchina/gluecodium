

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
#include "smoke/PseudoColor.h"

using PseudoColor = ::smoke::PseudoColor;



void register_smoke_PseudoColor(py::module_& module) {
auto cls_PseudoColor = py::class_<PseudoColor>(module, "smoke_PseudoColor")
        .def_readwrite("red", &PseudoColor::red)
        .def_readwrite("green", &PseudoColor::green)
        .def_readwrite("blue", &PseudoColor::blue)
        .def_readwrite("alpha", &PseudoColor::alpha)
        .def(py::init<>())
        .def(py::init<float, float, float, float>(), py::arg("red"), py::arg("green"), py::arg("blue"), py::arg("alpha"))
        .def("__eq__", [](const PseudoColor& lhs, const PseudoColor& rhs) { return lhs == rhs; })
        .def("__hash__", [](const PseudoColor& self) { return gluecodium::hash<PseudoColor>{}(self); })
        ;


}
