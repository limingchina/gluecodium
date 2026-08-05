

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
#include "smoke/CommentsTypeCollection.h"
#include "cstdint"

using CommentsTypeCollection = ::smoke::CommentsTypeCollection;
using TypeCollectionStruct = ::smoke::CommentsTypeCollection::TypeCollectionStruct;
using TypeCollectionEnum = ::smoke::CommentsTypeCollection::TypeCollectionEnum;



void register_smoke_CommentsTypeCollection(py::module_& module) {
auto cls_CommentsTypeCollection = py::class_<CommentsTypeCollection>(module, "smoke_CommentsTypeCollection")
        .def(py::init<>())
        ;

auto cls_CommentsTypeCollectionTypeCollectionStruct = py::class_<TypeCollectionStruct>(cls_CommentsTypeCollection, "TypeCollectionStruct")
        .def_readwrite("field", &TypeCollectionStruct::field)
        .def(py::init<>())
        .def(py::init<int32_t>(), py::arg("field"))
        ;

auto cls_CommentsTypeCollectionTypeCollectionEnum = py::enum_<TypeCollectionEnum>(cls_CommentsTypeCollection, "TypeCollectionEnum")
        .value("ITEM", TypeCollectionEnum::ITEM)
        ;


}
