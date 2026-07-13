

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/MutableStructNoClash.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using MutableStructNoClash = ::gluecodium::smoke::MutableStructNoClash;

void register_MutableStructNoClash(py::module_& module) {
    py::class_<MutableStructNoClash>(module, "MutableStructNoClash")
        .def_readwrite("string_field", &MutableStructNoClash::string_field)
        .def_readwrite("int_field", &MutableStructNoClash::int_field)
        .def_readwrite("bool_field", &MutableStructNoClash::bool_field)
        .def(py::init<>())
        ;
}

