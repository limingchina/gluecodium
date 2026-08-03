

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
#include "gluecodium/DurationHash.h"
#include "smoke/PosDefaultsWithDuration.h"
#include "chrono"

using PosDefaultsWithDuration = ::smoke::PosDefaultsWithDuration;



void register_smoke_PosDefaultsWithDuration(py::module_& module) {
auto cls_PosDefaultsWithDuration = py::class_<PosDefaultsWithDuration>(module, "smoke_PosDefaultsWithDuration")
        .def_readwrite("duration_field", &PosDefaultsWithDuration::duration_field)
        .def_readwrite("nanos_field", &PosDefaultsWithDuration::nanos_field)
        .def(py::init<>())
        .def(py::init<::std::chrono::seconds, ::std::chrono::seconds>(), py::arg("duration_field"), py::arg("nanos_field"))
        ;


}
