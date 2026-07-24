

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

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InternalError = ::smoke::CppRefReturnType::InternalError;

void register_smoke_CppRefReturnTypeInternalError(py::module_& module) {
    py::enum_<InternalError>(module, "CppRefReturnTypeInternalError")
        .value("FOO", InternalError::FOO)
        .value("BAR", InternalError::BAR)
        ;
}

