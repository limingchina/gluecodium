

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
#include "kotlin_smoke/TimeZone.h"
#include "cstdint"

using TimeZone = ::kotlin_smoke::TimeZone;



void register_kotlin_smoke_TimeZone(py::module_& module) {
auto cls_TimeZone = py::class_<TimeZone>(module, "kotlin_smoke_TimeZone")
        .def_readwrite("raw_offset", &TimeZone::raw_offset)
        .def(py::init<>())
        .def(py::init<int32_t>(), py::arg("raw_offset"))
        ;


}
