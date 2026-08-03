

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
#include "smoke/DartInternalElementsSkipped.h"
#include "string"

using DartInternalElementsSkipped = ::smoke::DartInternalElementsSkipped;



void register_smoke_DartInternalElementsSkipped(py::module_& module) {
auto cls_DartInternalElementsSkipped = py::class_<DartInternalElementsSkipped>(module, "smoke_DartInternalElementsSkipped")
        .def_readwrite("bool_field", &DartInternalElementsSkipped::bool_field)
        .def_readwrite("string_field", &DartInternalElementsSkipped::string_field)
        .def(py::init<>())
        .def(py::init<bool, ::std::string>(), py::arg("bool_field"), py::arg("string_field"))
        .def("foo", &DartInternalElementsSkipped::foo)
        ;


}
