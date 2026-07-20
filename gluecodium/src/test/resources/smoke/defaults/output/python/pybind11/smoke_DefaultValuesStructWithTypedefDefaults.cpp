

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/DefaultValues.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructWithTypedefDefaults = ::smoke::DefaultValues::StructWithTypedefDefaults;

void register_DefaultValuesStructWithTypedefDefaults(py::module_& module) {
    py::class_<StructWithTypedefDefaults>(module, "DefaultValuesStructWithTypedefDefaults")
        .def_readwrite("long_field", &StructWithTypedefDefaults::long_field)
        .def_readwrite("bool_field", &StructWithTypedefDefaults::bool_field)
        .def_readwrite("string_field", &StructWithTypedefDefaults::string_field)
        .def(py::init<>())
        ;
}

