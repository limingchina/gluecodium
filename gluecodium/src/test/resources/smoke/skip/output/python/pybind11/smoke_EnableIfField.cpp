

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/EnableIfField.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EnableIfField = ::smoke::EnableIfField;

void register_EnableIfField(py::module_& module) {
    py::class_<EnableIfField>(module, "EnableIfField")
        .def_readwrite("int_field", &EnableIfField::int_field)
        .def_readwrite("string_field", &EnableIfField::string_field)
        .def_readwrite("bool_field", &EnableIfField::bool_field)
        .def(py::init<int32_t, ::std::string, bool>(), py::arg("int_field"), py::arg("string_field"), py::arg("bool_field"))
        ;
}

