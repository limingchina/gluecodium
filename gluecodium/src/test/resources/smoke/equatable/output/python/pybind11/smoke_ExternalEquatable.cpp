

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
#include "foo/Bar.h"
#include "smoke/ExternalEquatable.h"
#include "string"

using ExternalEquatable = ::smoke::ExternalEquatable;
using ExternalEquatableStruct = ::smoke::ExternalEquatable::ExternalEquatableStruct;



void register_smoke_ExternalEquatable(py::module_& module) {
auto cls_ExternalEquatable = py::class_<ExternalEquatable>(module, "smoke_ExternalEquatable")
        .def(py::init<>())
        ;

auto cls_ExternalEquatableExternalEquatableStruct = py::class_<ExternalEquatableStruct>(cls_ExternalEquatable, "ExternalEquatableStruct")
        ;


}
