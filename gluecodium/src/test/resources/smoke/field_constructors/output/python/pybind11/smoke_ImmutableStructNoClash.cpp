

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ImmutableStructNoClash.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ImmutableStructNoClash = ::gluecodium::smoke::ImmutableStructNoClash;

void register_ImmutableStructNoClash(py::module_& module) {
    py::class_<ImmutableStructNoClash>(module, "ImmutableStructNoClash")
        .def_readwrite("string_field", &ImmutableStructNoClash::string_field)
        .def_readwrite("int_field", &ImmutableStructNoClash::int_field)
        .def_readwrite("bool_field", &ImmutableStructNoClash::bool_field)
        .def(py::init<>())
        .def(py::init<::std::string, int32_t, bool>(), py::arg("string_field"), py::arg("int_field"), py::arg("bool_field"))
        ;
}

