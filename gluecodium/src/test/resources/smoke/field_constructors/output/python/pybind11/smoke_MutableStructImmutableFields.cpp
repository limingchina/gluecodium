

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ImmutableStructNoClash.h"
#include "smoke/MutableStructImmutableFields.h"
#include "cstdint"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using MutableStructImmutableFields = ::smoke::MutableStructImmutableFields;

void register_MutableStructImmutableFields(py::module_& module) {
    py::class_<MutableStructImmutableFields>(module, "MutableStructImmutableFields")
        .def_readonly("struct_field", &MutableStructImmutableFields::struct_field)
        .def_readwrite("int_field", &MutableStructImmutableFields::int_field)
        .def_readwrite("bool_field", &MutableStructImmutableFields::bool_field)
        .def(py::init<>())
        ;
}

