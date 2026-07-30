

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
#include "smoke/DartDeprecatedPosDefaultsCustom.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DartDeprecatedPosDefaultsCustom = ::smoke::DartDeprecatedPosDefaultsCustom;

void register_smoke_DartDeprecatedPosDefaultsCustom(py::module_& module) {
    py::class_<DartDeprecatedPosDefaultsCustom>(module, "smoke_DartDeprecatedPosDefaultsCustom")
        .def_readwrite("int_field", &DartDeprecatedPosDefaultsCustom::int_field)
        .def_readwrite("string_field", &DartDeprecatedPosDefaultsCustom::string_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("string_field"))
        .def(py::init<int32_t, ::std::string>(), py::arg("int_field"), py::arg("string_field"))
        .def_static("custom", &DartDeprecatedPosDefaultsCustom::custom)
        ;
}

