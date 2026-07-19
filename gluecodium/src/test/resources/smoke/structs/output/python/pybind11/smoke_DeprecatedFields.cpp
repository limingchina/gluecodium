

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/DeprecatedFields.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DeprecatedFields = ::smoke::DeprecatedFields;

void register_DeprecatedFields(py::module_& module) {
    py::class_<DeprecatedFields>(module, "DeprecatedFields")
        .def_readwrite("normal_field1", &DeprecatedFields::normal_field1)
        .def_readwrite("deprecated_field", &DeprecatedFields::deprecated_field)
        .def_readwrite("normal_field2", &DeprecatedFields::normal_field2)
        .def(py::init<>())
        .def(py::init<::std::string, ::std::string, ::std::string>(), py::arg("normal_field1"), py::arg("deprecated_field"), py::arg("normal_field2"))
        ;
}

