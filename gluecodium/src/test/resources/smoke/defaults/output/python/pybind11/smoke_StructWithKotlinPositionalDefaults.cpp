

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/StructWithKotlinPositionalDefaults.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructWithKotlinPositionalDefaults = ::smoke::StructWithKotlinPositionalDefaults;

void register_smoke_StructWithKotlinPositionalDefaults(py::module_& module) {
    py::class_<StructWithKotlinPositionalDefaults>(module, "StructWithKotlinPositionalDefaults")
        .def_readwrite("first_init_field", &StructWithKotlinPositionalDefaults::first_init_field)
        .def_readwrite("first_free_field", &StructWithKotlinPositionalDefaults::first_free_field)
        .def_readwrite("second_init_field", &StructWithKotlinPositionalDefaults::second_init_field)
        .def_readwrite("second_free_field", &StructWithKotlinPositionalDefaults::second_free_field)
        .def_readwrite("third_init_field", &StructWithKotlinPositionalDefaults::third_init_field)
        .def(py::init<>())
        .def(py::init<::std::string, bool>(py::arg("first_free_field"), py::arg("second_free_field")))
        .def(py::init<int32_t, ::std::string, float, bool, ::std::string(), py::arg("first_init_field"), py::arg("first_free_field"), py::arg("second_init_field"), py::arg("second_free_field"), py::arg("third_init_field"))
        ;
}

