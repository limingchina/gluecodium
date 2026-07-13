

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/PublicFieldsMixedInit.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using PublicFieldsMixedInit = ::gluecodium::smoke::PublicFieldsMixedInit;

void register_PublicFieldsMixedInit(py::module_& module) {
    py::class_<PublicFieldsMixedInit>(module, "PublicFieldsMixedInit")
        .def_readwrite("public_field1", &PublicFieldsMixedInit::public_field1)
        .def_readwrite("public_field2", &PublicFieldsMixedInit::public_field2)
        .def_readwrite("internal_field", &PublicFieldsMixedInit::internal_field)
        .def(py::init<::std::string, ::std::string, ::std::string>(), py::arg("public_field1"), py::arg("public_field2"), py::arg("internal_field"))
        ;
}

