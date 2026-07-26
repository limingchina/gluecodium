

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
#include "smoke/PublicClass.h"
#include "smoke/PublicInterface.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InternalStruct = ::smoke::PublicInterface::InternalStruct;

void register_smoke_PublicInterfaceInternalStruct(py::module_& module) {
    py::class_<InternalStruct>(module, "smoke_PublicInterfaceInternalStruct")
        .def_readwrite("field_of_internal_type", &InternalStruct::field_of_internal_type)
        .def(py::init<>())
        .def(py::init<::smoke::PublicClass::InternalStruct>(), py::arg("field_of_internal_type"))
        ;
}

