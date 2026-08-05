

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
#include "smoke/StructsWithMethods.h"
#include "smoke/ValidationUtils.h"
#include "cstdint"

using StructsWithMethods = ::smoke::StructsWithMethods;
using Vector = ::smoke::StructsWithMethods::Vector;



void register_smoke_StructsWithMethods(py::module_& module) {
auto cls_StructsWithMethods = py::class_<StructsWithMethods>(module, "smoke_StructsWithMethods")
        .def(py::init<>())
        ;

auto cls_StructsWithMethodsVector = py::class_<Vector>(cls_StructsWithMethods, "Vector")
        .def_readwrite("x", &Vector::x)
        .def_readwrite("y", &Vector::y)
        .def(py::init<>())
        .def(py::init<double, double>(), py::arg("x"), py::arg("y"))
        .def("distance_to", &Vector::distance_to, py::arg("other"))
        .def("add", &Vector::add, py::arg("other"))
        .def_static("validate", &Vector::validate, py::arg("x"), py::arg("y"))
        .def_static("create", py::overload_cast<const double, const double>(Vector::create), py::arg("x"), py::arg("y"))
        .def_static("create", py::overload_cast<const ::smoke::StructsWithMethods::Vector&>(Vector::create), py::arg("other"))
        .def_static("create", py::overload_cast<const uint64_t>(Vector::create), py::arg("input"))
        ;


}
