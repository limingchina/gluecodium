

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
#include "smoke/Nullable.h"
#include "cstdint"
#include "optional"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using NullableIntsStruct = ::smoke::Nullable::NullableIntsStruct;

void register_smoke_NullableNullableIntsStruct(py::module_& module) {
    py::class_<NullableIntsStruct>(module, "smoke_NullableNullableIntsStruct")
        .def_readwrite("int8_field", &NullableIntsStruct::int8_field)
        .def_readwrite("int16_field", &NullableIntsStruct::int16_field)
        .def_readwrite("int32_field", &NullableIntsStruct::int32_field)
        .def_readwrite("int64_field", &NullableIntsStruct::int64_field)
        .def_readwrite("uint8_field", &NullableIntsStruct::uint8_field)
        .def_readwrite("uint16_field", &NullableIntsStruct::uint16_field)
        .def_readwrite("uint32_field", &NullableIntsStruct::uint32_field)
        .def_readwrite("uint64_field", &NullableIntsStruct::uint64_field)
        .def(py::init<>())
        .def(py::init<std::optional< int8_t >, std::optional< int16_t >, std::optional< int32_t >, std::optional< int64_t >, std::optional< uint8_t >, std::optional< uint16_t >, std::optional< uint32_t >, std::optional< uint64_t >>(), py::arg("int8_field"), py::arg("int16_field"), py::arg("int32_field"), py::arg("int64_field"), py::arg("uint8_field"), py::arg("uint16_field"), py::arg("uint32_field"), py::arg("uint64_field"))
        ;
}

