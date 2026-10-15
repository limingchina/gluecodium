

#include <Python.h>
#include <pybind11/pybind11.h>
#include "_opaque_types.h"
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
        .def_property("int_field", [](const ::external::IntStruct& self) -> decltype(auto) {
            return
                (self.int_field)
            ;
        }, [](::external::IntStruct& self, const int32_t value) {

                self.int_field = value;

        })
        .def(py::init<>())
        .def(py::init<int32_t>(), py::arg("int_field"))
        ;


}
