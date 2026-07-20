

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/TypesWithDefaults.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructWithDefaults = ::smoke::TypesWithDefaults::StructWithDefaults;

void register_TypesWithDefaultsStructWithDefaults(py::module_& module) {
    py::class_<StructWithDefaults>(module, "TypesWithDefaultsStructWithDefaults")
        .def_readwrite("int_field", &StructWithDefaults::int_field)
        .def_readwrite("uint_field", &StructWithDefaults::uint_field)
        .def_readwrite("float_field", &StructWithDefaults::float_field)
        .def_readwrite("double_field", &StructWithDefaults::double_field)
        .def_readwrite("bool_field", &StructWithDefaults::bool_field)
        .def_readwrite("string_field", &StructWithDefaults::string_field)
        .def(py::init<>())
        ;
}

