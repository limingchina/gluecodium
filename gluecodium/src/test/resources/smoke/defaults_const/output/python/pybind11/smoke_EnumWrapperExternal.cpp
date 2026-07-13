

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "foo/AlienEnum4.h"
#include "smoke/EnumWrapperExternal.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EnumWrapperExternal = ::gluecodium::smoke::EnumWrapperExternal;

void register_EnumWrapperExternal(py::module_& module) {
    py::class_<EnumWrapperExternal>(module, "EnumWrapperExternal")
        .def_readwrite("enum_field", &EnumWrapperExternal::enum_field)
        ;
}

