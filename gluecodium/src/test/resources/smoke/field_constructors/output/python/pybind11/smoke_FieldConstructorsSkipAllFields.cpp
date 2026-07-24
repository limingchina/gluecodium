

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FieldConstructorsSkipAllFields.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FieldConstructorsSkipAllFields = ::smoke::FieldConstructorsSkipAllFields;

void register_smoke_FieldConstructorsSkipAllFields(py::module_& module) {
    py::class_<FieldConstructorsSkipAllFields>(module, "FieldConstructorsSkipAllFields")
        .def_readonly("string_field", &FieldConstructorsSkipAllFields::string_field)
        .def_readonly("int_field", &FieldConstructorsSkipAllFields::int_field)
        .def(py::init<::std::string, int32_t(), py::arg("string_field"), py::arg("int_field"))
        ;
}

