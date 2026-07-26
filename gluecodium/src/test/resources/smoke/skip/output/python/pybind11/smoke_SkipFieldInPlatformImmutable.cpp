

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
#include "smoke/DummyStruct.h"
#include "smoke/SkipFieldInPlatformImmutable.h"
#include "cstdint"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SkipFieldInPlatformImmutable = ::smoke::SkipFieldInPlatformImmutable;

void register_smoke_SkipFieldInPlatformImmutable(py::module_& module) {
    py::class_<SkipFieldInPlatformImmutable>(module, "smoke_SkipFieldInPlatformImmutable")
        .def_readonly("int_field", &SkipFieldInPlatformImmutable::int_field)
        .def_readonly("string_field", &SkipFieldInPlatformImmutable::string_field)
        .def_readonly("bool_field", &SkipFieldInPlatformImmutable::bool_field)
        .def(py::init<int32_t, bool>(), py::arg("int_field"), py::arg("bool_field"))
        .def(py::init<int32_t, ::smoke::DummyStruct, bool>(), py::arg("int_field"), py::arg("string_field"), py::arg("bool_field"))
        .def(py::init<int32_t, ::smoke::DummyStruct, bool>(), py::arg("int_field"), py::arg("string_field"), py::arg("bool_field"))
        .def(py::init<int32_t, ::smoke::DummyStruct, bool>(), py::arg("int_field"), py::arg("string_field"), py::arg("bool_field"))
        ;
}

