

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
using ImmutableStructWithDefaults = ::smoke::TypesWithDefaults::ImmutableStructWithDefaults;

void register_TypesWithDefaultsImmutableStructWithDefaults(py::module_& module) {
    py::class_<ImmutableStructWithDefaults>(module, "TypesWithDefaultsImmutableStructWithDefaults")
        .def_readonly("int_field", &ImmutableStructWithDefaults::int_field)
        .def_readonly("uint_field", &ImmutableStructWithDefaults::uint_field)
        .def_readonly("float_field", &ImmutableStructWithDefaults::float_field)
        .def_readonly("double_field", &ImmutableStructWithDefaults::double_field)
        .def_readonly("bool_field", &ImmutableStructWithDefaults::bool_field)
        .def_readonly("string_field", &ImmutableStructWithDefaults::string_field)
        .def(py::init<int32_t, uint32_t, float, double, bool, ::std::string>(), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("double_field"), py::arg("bool_field"), py::arg("string_field"))
        ;
}

