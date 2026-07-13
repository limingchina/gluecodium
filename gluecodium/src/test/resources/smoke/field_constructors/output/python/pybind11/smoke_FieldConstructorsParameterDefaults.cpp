

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FieldConstructorsParameterDefaults.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FieldConstructorsParameterDefaults = ::smoke::FieldConstructorsParameterDefaults;

void register_FieldConstructorsParameterDefaults(py::module_& module) {
    py::class_<FieldConstructorsParameterDefaults>(module, "FieldConstructorsParameterDefaults")
        .def_readwrite("string_field", &FieldConstructorsParameterDefaults::string_field)
        .def_readwrite("int_field", &FieldConstructorsParameterDefaults::int_field)
        .def_readwrite("bool_field", &FieldConstructorsParameterDefaults::bool_field)
        ;
}

