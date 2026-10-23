

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
#include "foo/AlienEnum4.h"
#include "smoke/EnumWrapperExternal.h"

using EnumWrapperExternal = ::smoke::EnumWrapperExternal;



void register_smoke_EnumWrapperExternal(py::module_& module) {
auto cls_EnumWrapperExternal = py::class_<EnumWrapperExternal>(module, "smoke_EnumWrapperExternal")
        .def_property("enum_field", [](const EnumWrapperExternal& self) -> decltype(auto) {
            return
                (self.enum_field)
            ;
        }, [](EnumWrapperExternal& self, const foo::AlienEnum4 value) {

                self.enum_field = value;

        })
        .def(py::init<>())
        .def(py::init<foo::AlienEnum4>(), py::arg("enum_field"))
        ;


}
