

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
#include "smoke/PublicFieldsNone.h"
#include "string"

using PublicFieldsNone = ::smoke::PublicFieldsNone;



void register_smoke_PublicFieldsNone(py::module_& module) {
auto cls_PublicFieldsNone = py::class_<PublicFieldsNone>(module, "smoke_PublicFieldsNone")
        .def_property("_internal_field", [](const PublicFieldsNone& self) -> decltype(auto) {
            return
                (self.internal_field)
            ;
        }, [](PublicFieldsNone& self, const ::std::string& value) {

                self.internal_field = value;

        })
        .def(py::init<>())
        .def(py::init([]() {
            return PublicFieldsNone(::std::string{});
        }))
        ;


}
