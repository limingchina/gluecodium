

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/FooBarEnum.h"
#include "smoke/InternalEnumDefaults.h"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InternalEnumDefaults = ::smoke::InternalEnumDefaults;

void register_InternalEnumDefaults(py::module_& module) {
    py::class_<InternalEnumDefaults>(module, "InternalEnumDefaults")
        .def_readwrite("public_field", &InternalEnumDefaults::public_field)
        .def_readwrite("public_list_field", &InternalEnumDefaults::public_list_field)
        .def_readwrite("internal_field", &InternalEnumDefaults::internal_field)
        .def_readwrite("internal_list_field", &InternalEnumDefaults::internal_list_field)
        .def(py::init<>())
        ;
}

