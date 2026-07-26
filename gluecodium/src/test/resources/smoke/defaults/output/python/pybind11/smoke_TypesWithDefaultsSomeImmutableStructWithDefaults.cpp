

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
#include "smoke/TypesWithDefaults.h"
#include "cstdint"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SomeImmutableStructWithDefaults = ::smoke::TypesWithDefaults::SomeImmutableStructWithDefaults;

void register_smoke_TypesWithDefaultsSomeImmutableStructWithDefaults(py::module_& module) {
    py::class_<SomeImmutableStructWithDefaults>(module, "smoke_TypesWithDefaultsSomeImmutableStructWithDefaults")
        .def_readonly("int_field", &SomeImmutableStructWithDefaults::int_field)
        .def(py::init<>())
        .def(py::init<int32_t>(), py::arg("int_field"))
        ;
}

