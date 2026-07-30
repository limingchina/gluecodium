

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

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ImmutableStructWithFieldUsingImmutableStruct = ::smoke::TypesWithDefaults::ImmutableStructWithFieldUsingImmutableStruct;

void register_smoke_TypesWithDefaultsImmutableStructWithFieldUsingImmutableStruct(py::module_& module) {
    py::class_<ImmutableStructWithFieldUsingImmutableStruct>(module, "smoke_TypesWithDefaultsImmutableStructWithFieldUsingImmutableStruct")
        .def_readonly("some_field1", &ImmutableStructWithFieldUsingImmutableStruct::some_field1)
        .def_readonly("some_field2", &ImmutableStructWithFieldUsingImmutableStruct::some_field2)
        .def(py::init<>())
        .def(py::init<::smoke::TypesWithDefaults::SomeImmutableStructWithDefaults, ::smoke::TypesWithDefaults::ImmutableStructWithCollections>(), py::arg("some_field1"), py::arg("some_field2"))
        ;
}

