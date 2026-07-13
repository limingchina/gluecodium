

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/DefaultsWithFcStruct.h"
#include "smoke/FcStruct.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DefaultsWithFcStruct = ::gluecodium::smoke::DefaultsWithFcStruct;

void register_DefaultsWithFcStruct(py::module_& module) {
    py::class_<DefaultsWithFcStruct>(module, "DefaultsWithFcStruct")
        .def_readwrite("struct_field", &DefaultsWithFcStruct::struct_field)
        ;
}

