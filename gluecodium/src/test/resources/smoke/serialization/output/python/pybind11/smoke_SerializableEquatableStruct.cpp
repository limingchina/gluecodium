

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
#include "smoke/SerializableEquatableStruct.h"
#include "string"

using SerializableEquatableStruct = ::smoke::SerializableEquatableStruct;



void register_smoke_SerializableEquatableStruct(py::module_& module) {
auto cls_SerializableEquatableStruct = py::class_<SerializableEquatableStruct>(module, "smoke_SerializableEquatableStruct")
        .def_readwrite("foo_field", &SerializableEquatableStruct::foo_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("foo_field"))
        .def("__eq__", [](const SerializableEquatableStruct& lhs, const SerializableEquatableStruct& rhs) { return lhs == rhs; })
        .def("__hash__", [](const SerializableEquatableStruct& self) { return gluecodium::hash<SerializableEquatableStruct>{}(self); })
        ;


}
