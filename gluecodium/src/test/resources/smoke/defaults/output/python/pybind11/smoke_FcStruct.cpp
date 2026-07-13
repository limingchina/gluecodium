

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FcStruct.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FcStruct = ::gluecodium::smoke::FcStruct;

void register_FcStruct(py::module_& module) {
    py::class_<FcStruct>(module, "FcStruct")
        .def_readwrite("string_field", &FcStruct::string_field)
        ;
}

