

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ImmutableStructWithDefaults.h"
#include "cstdint"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ImmutableStructWithDefaults = ::smoke::ImmutableStructWithDefaults;

void register_ImmutableStructWithDefaults(py::module_& module) {
    py::class_<ImmutableStructWithDefaults>(module, "ImmutableStructWithDefaults")
        .def_readonly("int_field", &ImmutableStructWithDefaults::int_field)
        .def(py::init<>())
        ;
}

