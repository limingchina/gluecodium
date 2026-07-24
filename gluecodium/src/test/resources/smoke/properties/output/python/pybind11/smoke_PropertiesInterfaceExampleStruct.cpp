

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/PropertiesInterface.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ExampleStruct = ::smoke::PropertiesInterface::ExampleStruct;

void register_smoke_PropertiesInterfaceExampleStruct(py::module_& module) {
    py::class_<ExampleStruct>(module, "PropertiesInterfaceExampleStruct")
        .def_readwrite("value", &ExampleStruct::value)
        .def(py::init<>())
        .def(py::init<double(), py::arg("value"))
        ;
}

