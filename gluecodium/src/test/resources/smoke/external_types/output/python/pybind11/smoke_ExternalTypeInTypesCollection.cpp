

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
#include "include/ExternalTypeInTypesCollection.h"
#include "smoke/ExternalTypeInTypesCollection.h"
#include "cstdint"

using ExternalTypeInTypesCollection = ::smoke::ExternalTypeInTypesCollection;



void register_smoke_ExternalTypeInTypesCollection(py::module_& module) {
auto cls_ExternalTypeInTypesCollection = py::class_<ExternalTypeInTypesCollection>(module, "smoke_ExternalTypeInTypesCollection")
        .def(py::init<>())
        ;

auto cls_ExternalTypeInTypesCollectionIntStruct = py::class_<::external::IntStruct>(cls_ExternalTypeInTypesCollection, "IntStruct")
        ;


}
