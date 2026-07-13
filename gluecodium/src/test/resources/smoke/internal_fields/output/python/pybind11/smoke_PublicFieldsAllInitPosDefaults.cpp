

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/PublicFieldsAllInitPosDefaults.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using PublicFieldsAllInitPosDefaults = ::smoke::PublicFieldsAllInitPosDefaults;

void register_PublicFieldsAllInitPosDefaults(py::module_& module) {
    py::class_<PublicFieldsAllInitPosDefaults>(module, "PublicFieldsAllInitPosDefaults")
        .def_readwrite("public_field", &PublicFieldsAllInitPosDefaults::public_field)
        .def_readwrite("internal_field", &PublicFieldsAllInitPosDefaults::internal_field)
        .def(py::init<>())
        ;
}

