

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
#include "optional"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ImmutableStructWithNullableFieldUsingImmutableStruct = ::smoke::TypesWithDefaults::ImmutableStructWithNullableFieldUsingImmutableStruct;

void register_smoke_TypesWithDefaultsImmutableStructWithNullableFieldUsingImmutableStruct(py::module_& module) {
    py::class_<ImmutableStructWithNullableFieldUsingImmutableStruct>(module, "smoke_TypesWithDefaultsImmutableStructWithNullableFieldUsingImmutableStruct")
        .def_readonly("some_field1", &ImmutableStructWithNullableFieldUsingImmutableStruct::some_field1)
        .def_readonly("some_field2", &ImmutableStructWithNullableFieldUsingImmutableStruct::some_field2)
        .def(py::init<>())
        .def(py::init<std::optional< ::smoke::TypesWithDefaults::SomeImmutableStructWithDefaults >, std::optional< ::smoke::TypesWithDefaults::ImmutableStructWithCollections >>(), py::arg("some_field1"), py::arg("some_field2"))
        ;
}

