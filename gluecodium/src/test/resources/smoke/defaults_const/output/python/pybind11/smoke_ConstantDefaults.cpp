

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
#include "fire/SomeStruct.h"
#include "smoke/ConstantDefaults.h"

using ConstantDefaults = ::smoke::ConstantDefaults;



void register_smoke_ConstantDefaults(py::module_& module) {
auto cls_ConstantDefaults = py::class_<ConstantDefaults>(module, "smoke_ConstantDefaults")
        .def_property("field1", [](const ConstantDefaults& self) -> decltype(auto) {
            return
                (self.field1)
            ;
        }, [](ConstantDefaults& self, const ::fire::SomeStruct& value) {

                self.field1 = value;

        })
        .def_property("field2", [](const ConstantDefaults& self) -> decltype(auto) {
            return
                (self.field2)
            ;
        }, [](ConstantDefaults& self, const ::fire::SomeStruct& value) {

                self.field2 = value;

        })
        .def(py::init<>())
        .def(py::init<::fire::SomeStruct, ::fire::SomeStruct>(), py::arg("field1"), py::arg("field2"))
        ;


}
