

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
using PublicStructWithInternalDefaults = ::smoke::PublicClass::PublicStructWithInternalDefaults;

void register_PublicClassPublicStructWithInternalDefaults(py::module_& module) {
    py::class_<PublicStructWithInternalDefaults>(module, "PublicClassPublicStructWithInternalDefaults")
        .def_readwrite("internal_field", &PublicStructWithInternalDefaults::internal_field)
        .def_readwrite("public_field", &PublicStructWithInternalDefaults::public_field)
        .def(py::init<>())
        .def(py::init<::std::string, float>(), py::arg("internal_field"), py::arg("public_field"))
        ;
}

