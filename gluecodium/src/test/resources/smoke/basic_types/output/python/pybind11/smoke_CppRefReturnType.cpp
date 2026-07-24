

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/CppRefReturnType.h"
#include "memory"
#include "optional"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using CppRefReturnType = ::smoke::CppRefReturnType;


void register_smoke_CppRefReturnType(py::module_& module) {
    py::class_<CppRefReturnType, std::shared_ptr<CppRefReturnType>>(module, "CppRefReturnType")
        .def_static("string_property", &CppRefReturnType::get_string_property)
        ;
}

