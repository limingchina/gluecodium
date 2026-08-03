

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
#include "smoke/AsyncErrorCode.h"

using AsyncErrorCode = ::smoke::AsyncErrorCode;



void register_smoke_AsyncErrorCode(py::module_& module) {
auto cls_AsyncErrorCode = py::enum_<AsyncErrorCode>(module, "smoke_AsyncErrorCode")
        .value("VALUE1", AsyncErrorCode::VALUE1)
        ;


}
