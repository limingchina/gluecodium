

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/PublicFieldsNoInit.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using PublicFieldsNoInit = ::smoke::PublicFieldsNoInit;

void register_PublicFieldsNoInit(py::module_& module) {
    py::class_<PublicFieldsNoInit>(module, "PublicFieldsNoInit")
        .def_readwrite("public_field", &PublicFieldsNoInit::public_field)
        .def_readwrite("internal_field", &PublicFieldsNoInit::internal_field)
        .def(py::init<::std::string, ::std::string>(), py::arg("public_field"), py::arg("internal_field"))
        ;
}

