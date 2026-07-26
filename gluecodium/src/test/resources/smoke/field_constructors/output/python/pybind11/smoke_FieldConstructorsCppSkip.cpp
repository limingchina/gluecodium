

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
#include "smoke/FieldConstructorsCppSkip.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FieldConstructorsCppSkip = ::smoke::FieldConstructorsCppSkip;

void register_smoke_FieldConstructorsCppSkip(py::module_& module) {
    py::class_<FieldConstructorsCppSkip>(module, "smoke_FieldConstructorsCppSkip")
        .def_readwrite("string_field", &FieldConstructorsCppSkip::string_field)
        .def_readwrite("int_field", &FieldConstructorsCppSkip::int_field)
        .def(py::init<>())
        .def(py::init<::std::string, int32_t>(), py::arg("string_field"), py::arg("int_field"))
        .def(py::init<::std::string, int32_t>(), py::arg("string_field"), py::arg("int_field"))
        ;
}

