

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/PublicClass.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using PublicStruct = ::smoke::PublicClass::PublicStruct;

void register_PublicClassPublicStruct(py::module_& module) {
    py::class_<PublicStruct>(module, "PublicClassPublicStruct")
        .def_readwrite("internal_field", &PublicStruct::internal_field)
        .def(py::init<>())
        .def(py::init<::smoke::PublicClass::InternalStruct>(), py::arg("internal_field"))
        ;
}

