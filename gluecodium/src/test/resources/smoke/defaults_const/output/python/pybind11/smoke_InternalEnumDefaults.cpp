

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
#include "gluecodium/VectorHash.h"
#include "smoke/FooBarEnum.h"
#include "smoke/InternalEnumDefaults.h"
#include "vector"

using InternalEnumDefaults = ::smoke::InternalEnumDefaults;



void register_smoke_InternalEnumDefaults(py::module_& module) {
auto cls_InternalEnumDefaults = py::class_<InternalEnumDefaults>(module, "smoke_InternalEnumDefaults")
        .def_readwrite("public_field", &InternalEnumDefaults::public_field)
        .def_readwrite("public_list_field", &InternalEnumDefaults::public_list_field)
        .def_readwrite("_internal_field", &InternalEnumDefaults::internal_field)
        .def_readwrite("_internal_list_field", &InternalEnumDefaults::internal_list_field)
        .def(py::init<>())
        .def(py::init([](const ::smoke::FooBarEnum& public_field, const ::std::vector< ::smoke::FooBarEnum >& public_list_field) {
            return InternalEnumDefaults(public_field, public_list_field, ::smoke::FooBarEnum{}, ::std::vector< ::smoke::FooBarEnum >{});
        }), py::arg("public_field"), py::arg("public_list_field"))
        ;


}
