

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/Alias.h"
#include "smoke/EnumWithAlias.h"

void register_AliasError(py::module_& module) {
    py::exception<::std::error_code>(module, "AliasError");
}

