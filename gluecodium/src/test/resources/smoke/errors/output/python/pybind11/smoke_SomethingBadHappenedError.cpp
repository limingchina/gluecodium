

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SomeInternalEnum.h"
#include "smoke/SomethingBadHappened.h"

void register_SomethingBadHappenedError(py::module_& module) {
    py::exception<::std::error_code>(module, "SomethingBadHappenedError");
}

