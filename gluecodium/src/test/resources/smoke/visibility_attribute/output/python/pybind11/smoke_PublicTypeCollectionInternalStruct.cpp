

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

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InternalStruct = ::smoke::PublicTypeCollection::InternalStruct;

void register_smoke_PublicTypeCollectionInternalStruct(py::module_& module) {
    py::class_<InternalStruct>(module, "smoke_PublicTypeCollectionInternalStruct")
        .def_readwrite("string_field", &InternalStruct::string_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("string_field"))
        .def("foo_bar", &InternalStruct::foo_bar)
        ;
}

