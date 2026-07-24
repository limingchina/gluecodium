

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/CalculatorListener.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ResultStruct = ::smoke::CalculatorListener::ResultStruct;

void register_smoke_CalculatorListenerResultStruct(py::module_& module) {
    py::class_<ResultStruct>(module, "CalculatorListenerResultStruct")
        .def_readwrite("result", &ResultStruct::result)
        .def(py::init<>())
        .def(py::init<double(), py::arg("result"))
        ;
}

