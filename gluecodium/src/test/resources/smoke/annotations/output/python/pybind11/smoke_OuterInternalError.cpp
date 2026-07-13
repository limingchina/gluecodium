

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/OuterInternal.h"
#include "smoke/OuterInternalEnum.h"

void register_OuterInternalError(py::module_& module) {
    py::exception<::std::error_code>(module, "OuterInternalError");
}

