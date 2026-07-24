

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/InternalClassWithFunctions.h"
#include "memory"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InternalClassWithFunctions = ::smoke::InternalClassWithFunctions;


void register_smoke_InternalClassWithFunctions(py::module_& module) {
    py::class_<InternalClassWithFunctions, std::shared_ptr<InternalClassWithFunctions>>(module, "InternalClassWithFunctions")
        .def(py::init<>())

        .def_static("make", py::overload_cast<>(&InternalClassWithFunctions::make))
        .def(py::init<::std::string>(py::arg("foo")))

        .def_static("make", py::overload_cast<const ::std::string&>(&InternalClassWithFunctions::make), py::arg("foo"))
        ;
}

