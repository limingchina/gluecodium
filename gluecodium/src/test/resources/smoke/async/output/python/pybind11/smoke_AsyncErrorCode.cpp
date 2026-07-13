

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/AsyncErrorCode.h"

void register_AsyncErrorCode(py::module_& module) {
    py::enum_<AsyncErrorCode>(module, "AsyncErrorCode")
        .value("VALUE1", AsyncErrorCode::VALUE1)
        ;
}

