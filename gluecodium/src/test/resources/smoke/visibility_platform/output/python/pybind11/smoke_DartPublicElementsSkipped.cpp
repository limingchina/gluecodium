

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/DartPublicElementsSkipped.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DartPublicElementsSkipped = ::gluecodium::smoke::DartPublicElementsSkipped;

void register_DartPublicElementsSkipped(py::module_& module) {
    py::class_<DartPublicElementsSkipped>(module, "DartPublicElementsSkipped")
        .def_readwrite("bool_field", &DartPublicElementsSkipped::bool_field)
        .def_readwrite("string_field", &DartPublicElementsSkipped::string_field)
        .def(py::init<bool, ::std::string>(), py::arg("bool_field"), py::arg("string_field"))
        .def("foo", &DartPublicElementsSkipped::foo)
        ;
}

