

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ListenerWithProperties.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ResultStruct = ::smoke::ListenerWithProperties::ResultStruct;

void register_ListenerWithPropertiesResultStruct(py::module_& module) {
    py::class_<ResultStruct>(module, "ListenerWithPropertiesResultStruct")
        .def_readwrite("result", &ResultStruct::result)
        .def(py::init<>())
        .def(py::init<double>(), py::arg("result"))
        ;
}

