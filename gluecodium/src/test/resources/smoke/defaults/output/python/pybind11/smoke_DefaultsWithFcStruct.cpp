

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
#include "smoke/DefaultsWithFcStruct.h"
#include "smoke/FcStruct.h"

using DefaultsWithFcStruct = ::smoke::DefaultsWithFcStruct;



void register_smoke_DefaultsWithFcStruct(py::module_& module) {
auto cls_DefaultsWithFcStruct = py::class_<DefaultsWithFcStruct>(module, "smoke_DefaultsWithFcStruct")
        .def_property("struct_field", [](const DefaultsWithFcStruct& self) -> decltype(auto) {
            return
                (self.struct_field)
            ;
        }, [](DefaultsWithFcStruct& self, const ::smoke::FcStruct& value) {

                self.struct_field = value;

        })
        .def(py::init<>())
        ;


}
