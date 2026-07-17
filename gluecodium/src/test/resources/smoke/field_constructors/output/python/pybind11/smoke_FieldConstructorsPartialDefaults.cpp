

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FieldConstructorsPartialDefaults.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FieldConstructorsPartialDefaults = ::smoke::FieldConstructorsPartialDefaults;

void register_FieldConstructorsPartialDefaults(py::module_& module) {
    py::class_<FieldConstructorsPartialDefaults>(module, "FieldConstructorsPartialDefaults")
        .def_readwrite("string_field", &FieldConstructorsPartialDefaults::string_field)
        .def_readwrite("int_field", &FieldConstructorsPartialDefaults::int_field)
        .def_readwrite("bool_field", &FieldConstructorsPartialDefaults::bool_field)
        .def(py::init<>())
        .def(py::init<int32_t, ::std::string>(), py::arg("int_field"), py::arg("string_field"))
        .def(py::init<bool, int32_t, ::std::string>(), py::arg("bool_field"), py::arg("int_field"), py::arg("string_field"))
        ;
}

