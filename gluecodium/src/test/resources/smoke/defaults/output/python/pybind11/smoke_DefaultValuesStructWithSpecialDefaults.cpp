

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/DefaultValues.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructWithSpecialDefaults = ::smoke::DefaultValues::StructWithSpecialDefaults;

void register_smoke_DefaultValuesStructWithSpecialDefaults(py::module_& module) {
    py::class_<StructWithSpecialDefaults>(module, "smoke_DefaultValuesStructWithSpecialDefaults")
        .def_readwrite("float_nan_field", &StructWithSpecialDefaults::float_nan_field)
        .def_readwrite("float_infinity_field", &StructWithSpecialDefaults::float_infinity_field)
        .def_readwrite("float_negative_infinity_field", &StructWithSpecialDefaults::float_negative_infinity_field)
        .def_readwrite("double_nan_field", &StructWithSpecialDefaults::double_nan_field)
        .def_readwrite("double_infinity_field", &StructWithSpecialDefaults::double_infinity_field)
        .def_readwrite("double_negative_infinity_field", &StructWithSpecialDefaults::double_negative_infinity_field)
        .def(py::init<>())
        .def(py::init<float, float, float, double, double, double>(), py::arg("float_nan_field"), py::arg("float_infinity_field"), py::arg("float_negative_infinity_field"), py::arg("double_nan_field"), py::arg("double_infinity_field"), py::arg("double_negative_infinity_field"))
        ;
}

