

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
#include "fire/Enum4.h"
#include "smoke/EnumWrapper.h"

using EnumWrapper = ::smoke::EnumWrapper;



void register_smoke_EnumWrapper(py::module_& module) {
auto cls_EnumWrapper = py::class_<EnumWrapper>(module, "smoke_EnumWrapper")
        .def_property("enum_field", [](const EnumWrapper& self) -> decltype(auto) {
            return
                (self.enum_field)
            ;
        }, [](EnumWrapper& self, const ::fire::Enum4 value) {

                self.enum_field = value;

        })
        .def(py::init<>())
        .def(py::init<::fire::Enum4>(), py::arg("enum_field"))
        ;


}
