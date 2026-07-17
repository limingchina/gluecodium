

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FieldConstructorsInternal.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FieldConstructorsInternal = ::smoke::FieldConstructorsInternal;

void register_FieldConstructorsInternal(py::module_& module) {
    py::class_<FieldConstructorsInternal>(module, "FieldConstructorsInternal")
        .def_readwrite("public_field", &FieldConstructorsInternal::public_field)
        .def_readwrite("internal_field", &FieldConstructorsInternal::internal_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("public_field"))
        .def(py::init<double>(), py::arg("internal_field"))
        .def(py::init<double, ::std::string>(), py::arg("internal_field"), py::arg("public_field"))
        ;
}

