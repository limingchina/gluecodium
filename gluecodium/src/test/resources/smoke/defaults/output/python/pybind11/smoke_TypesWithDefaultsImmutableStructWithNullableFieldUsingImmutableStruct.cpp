

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/TypesWithDefaults.h"
#include "optional"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ImmutableStructWithNullableFieldUsingImmutableStruct = ::smoke::TypesWithDefaults::ImmutableStructWithNullableFieldUsingImmutableStruct;

void register_TypesWithDefaultsImmutableStructWithNullableFieldUsingImmutableStruct(py::module_& module) {
    py::class_<ImmutableStructWithNullableFieldUsingImmutableStruct>(module, "TypesWithDefaultsImmutableStructWithNullableFieldUsingImmutableStruct")
        .def_readonly("some_field1", &ImmutableStructWithNullableFieldUsingImmutableStruct::some_field1)
        .def_readonly("some_field2", &ImmutableStructWithNullableFieldUsingImmutableStruct::some_field2)
        .def(py::init<>())
        ;
}

