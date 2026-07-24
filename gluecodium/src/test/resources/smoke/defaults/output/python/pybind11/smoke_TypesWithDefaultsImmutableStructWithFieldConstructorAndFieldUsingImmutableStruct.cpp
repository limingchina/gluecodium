

#include <Python.h>
#include <pybind11/pybind11.h>
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
using ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct = ::smoke::TypesWithDefaults::ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct;

void register_smoke_TypesWithDefaultsImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct(py::module_& module) {
    py::class_<ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct>(module, "TypesWithDefaultsImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct")
        .def_readonly("some_field1", &ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct::some_field1)
        .def_readonly("some_field2", &ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct::some_field2)
        .def_readonly("some_field", &ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct::some_field)
        .def_readonly("another_field", &ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct::another_field)
        .def(py::init<>())
        .def(py::init<::smoke::TypesWithDefaults::SomeImmutableStructWithDefaults, ::smoke::TypesWithDefaults::ImmutableStructWithCollections, int32_t, int32_t(), py::arg("some_field1"), py::arg("some_field2"), py::arg("some_field"), py::arg("another_field"))
        .def(py::init<int32_t, int32_t(), py::arg("some_field"), py::arg("another_field"))
        ;
}

