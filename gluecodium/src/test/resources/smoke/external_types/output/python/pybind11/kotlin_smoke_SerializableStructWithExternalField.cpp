

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "kotlin_smoke/ExternalMarkedAsSerializable.h"
#include "kotlin_smoke/SerializableStructWithExternalField.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SerializableStructWithExternalField = ::gluecodium::kotlin_smoke::SerializableStructWithExternalField;

void register_SerializableStructWithExternalField(py::module_& module) {
    py::class_<SerializableStructWithExternalField>(module, "SerializableStructWithExternalField")
        .def_readwrite("some_struct", &SerializableStructWithExternalField::some_struct)
        .def(py::init<::kotlin_smoke::ExternalMarkedAsSerializable>(), py::arg("some_struct"))
        ;
}

