

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "kotlin_smoke/ExternalMarkedAsSerializable.h"
#include "kotlin_smoke/SerializableStructWithExternalField.h"

using SerializableStructWithExternalField = ::kotlin_smoke::SerializableStructWithExternalField;



void register_kotlin_smoke_SerializableStructWithExternalField(py::module_& module) {
auto cls_SerializableStructWithExternalField = py::class_<SerializableStructWithExternalField>(module, "kotlin_smoke_SerializableStructWithExternalField")
        .def_readwrite("some_struct", &SerializableStructWithExternalField::some_struct)
        .def(py::init<>())
        .def(py::init<::kotlin_smoke::ExternalMarkedAsSerializable>(), py::arg("some_struct"))
        ;


}
