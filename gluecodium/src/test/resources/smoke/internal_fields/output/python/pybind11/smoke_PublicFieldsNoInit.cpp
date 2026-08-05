

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
#include "smoke/PublicFieldsNoInit.h"
#include "string"

using PublicFieldsNoInit = ::smoke::PublicFieldsNoInit;



void register_smoke_PublicFieldsNoInit(py::module_& module) {
auto cls_PublicFieldsNoInit = py::class_<PublicFieldsNoInit>(module, "smoke_PublicFieldsNoInit")
        .def_readwrite("public_field", &PublicFieldsNoInit::public_field)
        .def_readwrite("_internal_field", &PublicFieldsNoInit::internal_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("public_field"))
        .def(py::init([](const ::std::string& public_field) {
            return PublicFieldsNoInit(public_field, ::std::string{});
        }), py::arg("public_field"))
        ;


}
