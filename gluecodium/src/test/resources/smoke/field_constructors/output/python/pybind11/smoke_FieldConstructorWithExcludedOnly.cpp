

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FieldConstructorWithExcludedOnly.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FieldConstructorWithExcludedOnly = ::smoke::FieldConstructorWithExcludedOnly;

void register_smoke_FieldConstructorWithExcludedOnly(py::module_& module) {
    py::class_<FieldConstructorWithExcludedOnly>(module, "FieldConstructorWithExcludedOnly")
        .def_readwrite("string_field", &FieldConstructorWithExcludedOnly::string_field)
        .def(py::init<>())
        .def(py::init<::std::string(), py::arg("string_field"))
        ;
}

