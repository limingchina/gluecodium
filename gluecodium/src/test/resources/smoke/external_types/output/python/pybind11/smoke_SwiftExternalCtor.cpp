

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
#include "smoke/SwiftExternalCtor.h"
#include "string"

using SwiftExternalCtor = ::smoke::SwiftExternalCtor;



void register_smoke_SwiftExternalCtor(py::module_& module) {
auto cls_SwiftExternalCtor = py::class_<SwiftExternalCtor>(module, "smoke_SwiftExternalCtor")
        .def_readwrite("field", &SwiftExternalCtor::field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("field"))
        .def_static("make", &SwiftExternalCtor::make, py::arg("field"))
        ;


}
