

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SkipEnableParameters.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SkipEnableParameters = ::gluecodium::smoke::SkipEnableParameters;

void register_SkipEnableParameters(py::module_& module) {
    py::class_<SkipEnableParameters>(module, "SkipEnableParameters")
        .def("do_something", &SkipEnableParameters::do_something, py::arg("input"))
        ;
}

