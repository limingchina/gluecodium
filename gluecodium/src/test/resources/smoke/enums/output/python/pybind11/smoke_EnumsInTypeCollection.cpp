

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
#include "smoke/EnumsInTypeCollection.h"

using EnumsInTypeCollection = ::smoke::EnumsInTypeCollection;
using TCEnum = ::smoke::EnumsInTypeCollection::TCEnum;



void register_smoke_EnumsInTypeCollection(py::module_& module) {
auto cls_EnumsInTypeCollection = py::class_<EnumsInTypeCollection>(module, "smoke_EnumsInTypeCollection")
        .def(py::init<>())
        ;

auto cls_EnumsInTypeCollectionTCEnum = py::enum_<TCEnum>(cls_EnumsInTypeCollection, "TCEnum")
        .value("FIRST", TCEnum::FIRST)
        .value("SECOND", TCEnum::SECOND)
        ;


}
