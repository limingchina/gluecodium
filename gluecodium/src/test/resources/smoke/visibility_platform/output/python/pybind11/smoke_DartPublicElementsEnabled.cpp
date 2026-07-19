

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/DartPublicElementsEnabled.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DartPublicElementsEnabled = ::smoke::DartPublicElementsEnabled;

void register_DartPublicElementsEnabled(py::module_& module) {
    py::class_<DartPublicElementsEnabled>(module, "DartPublicElementsEnabled")
        .def_readwrite("bool_field", &DartPublicElementsEnabled::bool_field)
        .def_readwrite("string_field", &DartPublicElementsEnabled::string_field)
        .def(py::init<>())
        .def(py::init<bool, ::std::string>(), py::arg("bool_field"), py::arg("string_field"))
        .def("foo", &DartPublicElementsEnabled::foo)

        ;
}

