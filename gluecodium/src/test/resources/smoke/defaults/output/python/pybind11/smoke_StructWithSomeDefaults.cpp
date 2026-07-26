

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
#include "smoke/StructWithSomeDefaults.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructWithSomeDefaults = ::smoke::StructWithSomeDefaults;

void register_smoke_StructWithSomeDefaults(py::module_& module) {
    py::class_<StructWithSomeDefaults>(module, "smoke_StructWithSomeDefaults")
        .def_readwrite("int_field", &StructWithSomeDefaults::int_field)
        .def_readwrite("string_field", &StructWithSomeDefaults::string_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("string_field"))
        .def(py::init<int32_t, ::std::string>(), py::arg("int_field"), py::arg("string_field"))
        .def(py::init<int32_t, ::std::string>(), py::arg("int_field"), py::arg("string_field"))
        ;
}

