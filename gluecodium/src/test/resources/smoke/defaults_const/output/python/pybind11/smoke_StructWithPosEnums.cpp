

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
#include "smoke/SomethingEnum.h"
#include "smoke/StructWithPosEnums.h"

using StructWithPosEnums = ::smoke::StructWithPosEnums;



void register_smoke_StructWithPosEnums(py::module_& module) {
auto cls_StructWithPosEnums = py::class_<StructWithPosEnums>(module, "smoke_StructWithPosEnums")
        .def_property("first_field", [](const StructWithPosEnums& self) -> decltype(auto) {
            return
                (self.first_field)
            ;
        }, [](StructWithPosEnums& self, const ::smoke::SomethingEnum value) {

                self.first_field = value;

        })
        .def_property("explicit_field", [](const StructWithPosEnums& self) -> decltype(auto) {
            return
                (self.explicit_field)
            ;
        }, [](StructWithPosEnums& self, const ::smoke::SomethingEnum value) {

                self.explicit_field = value;

        })
        .def_property("last_field", [](const StructWithPosEnums& self) -> decltype(auto) {
            return
                (self.last_field)
            ;
        }, [](StructWithPosEnums& self, const ::smoke::SomethingEnum value) {

                self.last_field = value;

        })
        .def(py::init<>())
        .def(py::init<::smoke::SomethingEnum, ::smoke::SomethingEnum, ::smoke::SomethingEnum>(), py::arg("first_field"), py::arg("explicit_field"), py::arg("last_field"))
        ;


}
