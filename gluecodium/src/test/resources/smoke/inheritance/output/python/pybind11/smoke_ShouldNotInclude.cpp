

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
#include "smoke/ShouldNotInclude.h"
#include "string"

using ShouldNotInclude = ::smoke::ShouldNotInclude;



void register_smoke_ShouldNotInclude(py::module_& module) {
auto cls_ShouldNotInclude = py::class_<ShouldNotInclude>(module, "smoke_ShouldNotInclude")
        .def_readwrite("field", &ShouldNotInclude::field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("field"))
        ;


}
