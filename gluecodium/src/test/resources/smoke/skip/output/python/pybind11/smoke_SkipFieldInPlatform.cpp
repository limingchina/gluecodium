

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SkipFieldInPlatform.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SkipFieldInPlatform = ::gluecodium::smoke::SkipFieldInPlatform;

void register_SkipFieldInPlatform(py::module_& module) {
    py::class_<SkipFieldInPlatform>(module, "SkipFieldInPlatform")
        .def_readwrite("int_field", &SkipFieldInPlatform::int_field)
        .def_readwrite("string_field", &SkipFieldInPlatform::string_field)
        .def_readwrite("bool_field", &SkipFieldInPlatform::bool_field)
        ;
}

