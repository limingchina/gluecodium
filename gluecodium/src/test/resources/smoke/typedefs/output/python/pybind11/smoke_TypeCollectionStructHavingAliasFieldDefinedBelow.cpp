

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
#include "smoke/TypeCollection.h"
#include "cstdint"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructHavingAliasFieldDefinedBelow = ::smoke::TypeCollection::StructHavingAliasFieldDefinedBelow;

void register_smoke_TypeCollectionStructHavingAliasFieldDefinedBelow(py::module_& module) {
    py::class_<StructHavingAliasFieldDefinedBelow>(module, "smoke_TypeCollectionStructHavingAliasFieldDefinedBelow")
        .def_readwrite("field", &StructHavingAliasFieldDefinedBelow::field)
        .def(py::init<>())
        .def(py::init<uint64_t>(), py::arg("field"))
        ;
}

