

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FieldConstructorsInternalFields.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FieldConstructorsInternalFields = ::gluecodium::smoke::FieldConstructorsInternalFields;

void register_FieldConstructorsInternalFields(py::module_& module) {
    py::class_<FieldConstructorsInternalFields>(module, "FieldConstructorsInternalFields")
        .def_readwrite("string_field", &FieldConstructorsInternalFields::string_field)
        .def_readwrite("int_field", &FieldConstructorsInternalFields::int_field)
        .def_readwrite("bool_field", &FieldConstructorsInternalFields::bool_field)
        ;
}

