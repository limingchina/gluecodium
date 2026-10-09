

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
#include "smoke/SerializableEquatableStruct.h"
#include "string"

using SerializableEquatableStruct = ::smoke::SerializableEquatableStruct;



void register_smoke_SerializableEquatableStruct(py::module_& module) {
auto cls_SerializableEquatableStruct = py::class_<SerializableEquatableStruct>(module, "smoke_SerializableEquatableStruct")
        .def_property("foo_field", [](const SerializableEquatableStruct& self) -> decltype(auto) {
            return
                (self.foo_field)
            ;
        }, [](SerializableEquatableStruct& self, const ::std::string& value) {

                self.foo_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("foo_field"))
        .def("__gluecodium_copy__", [](const SerializableEquatableStruct& self) { return SerializableEquatableStruct(self); })
        .def("__gluecodium_equals__", [](const SerializableEquatableStruct& lhs, const SerializableEquatableStruct& rhs) { return lhs == rhs; })
        .def("__gluecodium_hash__", [](const SerializableEquatableStruct& self) { return gluecodium::hash<SerializableEquatableStruct>{}(self); })
        ;


}
