

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
#include "smoke/Errors.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InternalErrorCode = ::smoke::Errors::InternalErrorCode;

void register_smoke_ErrorsInternalErrorCode(py::module_& module) {
    py::enum_<InternalErrorCode>(module, "smoke_ErrorsInternalErrorCode")
        .value("ERROR_NONE", InternalErrorCode::ERROR_NONE)
        .value("ERROR_FATAL", InternalErrorCode::ERROR_FATAL)
        ;
}

