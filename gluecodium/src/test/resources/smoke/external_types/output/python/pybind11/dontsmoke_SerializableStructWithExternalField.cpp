

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
#include "dontsmoke/ExternalMarkedAsSerializable.h"
#include "dontsmoke/SerializableStructWithExternalField.h"

using SerializableStructWithExternalField = ::dontsmoke::SerializableStructWithExternalField;



void register_dontsmoke_SerializableStructWithExternalField(py::module_& module) {
auto cls_SerializableStructWithExternalField = py::class_<SerializableStructWithExternalField>(module, "dontsmoke_SerializableStructWithExternalField")
        .def_readwrite("some_struct", &SerializableStructWithExternalField::some_struct)
        .def(py::init<>())
        .def(py::init<::dontsmoke::ExternalMarkedAsSerializable>(), py::arg("some_struct"))
        ;


}
