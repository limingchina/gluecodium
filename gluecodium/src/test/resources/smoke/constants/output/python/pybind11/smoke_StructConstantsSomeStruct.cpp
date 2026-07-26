

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
#include "smoke/StructConstants.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SomeStruct = ::smoke::StructConstants::SomeStruct;

void register_smoke_StructConstantsSomeStruct(py::module_& module) {
    py::class_<SomeStruct>(module, "smoke_StructConstantsSomeStruct")
        .def_readwrite("string_field", &SomeStruct::string_field)
        .def_readwrite("float_field", &SomeStruct::float_field)
        .def(py::init<>())
        .def(py::init<::std::string, float>(), py::arg("string_field"), py::arg("float_field"))
        .def(py::init<::std::string, float>(), py::arg("string_field"), py::arg("float_field"))
        ;
}

