

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "dontsmoke/ExternalMarkedAsSerializable.h"
#include "dontsmoke/SerializableStructWithExternalField.h"

void register_SerializableStructWithExternalField(py::module_& module) {
    py::class_<SerializableStructWithExternalField>(module, "SerializableStructWithExternalField")
        .def_readwrite("some_struct", &SerializableStructWithExternalField::some_struct)
        ;
}

