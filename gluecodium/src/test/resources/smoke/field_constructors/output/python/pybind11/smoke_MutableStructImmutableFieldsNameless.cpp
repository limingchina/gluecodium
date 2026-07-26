

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
#include "smoke/ImmutableNamelessCtor.h"
#include "smoke/MutableStructImmutableFieldsNameless.h"
#include "cstdint"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using MutableStructImmutableFieldsNameless = ::smoke::MutableStructImmutableFieldsNameless;

void register_smoke_MutableStructImmutableFieldsNameless(py::module_& module) {
    py::class_<MutableStructImmutableFieldsNameless>(module, "smoke_MutableStructImmutableFieldsNameless")
        .def_readwrite("struct_field", &MutableStructImmutableFieldsNameless::struct_field)
        .def_readwrite("int_field", &MutableStructImmutableFieldsNameless::int_field)
        .def_readwrite("bool_field", &MutableStructImmutableFieldsNameless::bool_field)
        .def(py::init<>())
        ;
}

