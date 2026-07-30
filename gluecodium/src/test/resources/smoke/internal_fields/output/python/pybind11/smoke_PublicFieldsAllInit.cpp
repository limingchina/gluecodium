

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
#include "smoke/PublicFieldsAllInit.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using PublicFieldsAllInit = ::smoke::PublicFieldsAllInit;

void register_smoke_PublicFieldsAllInit(py::module_& module) {
    py::class_<PublicFieldsAllInit>(module, "smoke_PublicFieldsAllInit")
        .def_readwrite("public_field", &PublicFieldsAllInit::public_field)
        .def(py::init<>())
        .def(py::init([](const ::std::string& public_field) {
            return PublicFieldsAllInit(public_field, ::std::string{});
        }), py::arg("public_field"))
        ;
}

