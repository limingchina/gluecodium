

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
#include "smoke/UnusedTopLevelPoint.h"
#include "string"

using UnusedTopLevelPoint = ::smoke::UnusedTopLevelPoint;



void register_smoke_UnusedTopLevelPoint(py::module_& module) {
auto cls_UnusedTopLevelPoint = py::class_<UnusedTopLevelPoint>(module, "smoke_UnusedTopLevelPoint")
        .def_readwrite("foo", &UnusedTopLevelPoint::foo)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("foo"))
        ;


}
