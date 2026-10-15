

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
#include "fire/AmbiguousEnum.h"
#include "fire/SomeStruct.h"
#include "smoke/AmbiguousDefaults.h"

using AmbiguousDefaults = ::smoke::AmbiguousDefaults;



void register_smoke_AmbiguousDefaults(py::module_& module) {
auto cls_AmbiguousDefaults = py::class_<AmbiguousDefaults>(module, "smoke_AmbiguousDefaults")
        .def_property("field1", [](const AmbiguousDefaults& self) -> decltype(auto) {
            return
                (self.field1)
            ;
        }, [](AmbiguousDefaults& self, const ::fire::AmbiguousEnum value) {

                self.field1 = value;

        })
        .def_property("field2", [](const AmbiguousDefaults& self) -> decltype(auto) {
            return
                (self.field2)
            ;
        }, [](AmbiguousDefaults& self, const ::fire::SomeStruct& value) {

                self.field2 = value;

        })
        .def(py::init<>())
        .def(py::init<::fire::AmbiguousEnum, ::fire::SomeStruct>(), py::arg("field1"), py::arg("field2"))
        ;


}
