

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/Async.h"
#include "smoke/AsyncErrorCode.h"

void register_AsyncError(py::module_& module) {
    py::exception<::std::error_code>(module, "AsyncError");
}

