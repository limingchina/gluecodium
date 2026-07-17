

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ImmutableStructWithClash.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ImmutableStructWithClash = ::smoke::ImmutableStructWithClash;

void register_ImmutableStructWithClash(py::module_& module) {
    py::class_<ImmutableStructWithClash>(module, "ImmutableStructWithClash")
        .def_readonly("string_field", &ImmutableStructWithClash::string_field)
        .def_readonly("int_field", &ImmutableStructWithClash::int_field)
        .def_readonly("bool_field", &ImmutableStructWithClash::bool_field)
        .def(py::init<>())
        .def(py::init<bool, int32_t, ::std::string>(), py::arg("bool_field"), py::arg("int_field"), py::arg("string_field"))
        ;
}

