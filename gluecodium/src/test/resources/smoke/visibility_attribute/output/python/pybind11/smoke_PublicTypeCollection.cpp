

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/PublicTypeCollection.h"
#include "string"

using PublicTypeCollection = ::smoke::PublicTypeCollection;
using InternalStruct = ::smoke::PublicTypeCollection::InternalStruct;



void register_smoke_PublicTypeCollection(py::module_& module) {
auto cls_PublicTypeCollection = py::class_<PublicTypeCollection>(module, "smoke_PublicTypeCollection")
        .def(py::init<>())
        ;

auto cls__PublicTypeCollectionInternalStruct = py::class_<InternalStruct>(cls_PublicTypeCollection, "_InternalStruct")
        .def_readwrite("_string_field", &InternalStruct::string_field)
        .def(py::init<>())
        .def(py::init([]() {
            return InternalStruct(::std::string{});
        }))
        .def("foo_bar", &InternalStruct::foo_bar)
        ;


}
