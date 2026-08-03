

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/DartExternalCtor.h"
#include "string"

using DartExternalCtor = ::smoke::DartExternalCtor;



void register_smoke_DartExternalCtor(py::module_& module) {
auto cls_DartExternalCtor = py::class_<DartExternalCtor>(module, "smoke_DartExternalCtor")
        .def_readwrite("field", &DartExternalCtor::field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("field"))
        .def_static("make", &DartExternalCtor::make, py::arg("field"))
        ;


}
