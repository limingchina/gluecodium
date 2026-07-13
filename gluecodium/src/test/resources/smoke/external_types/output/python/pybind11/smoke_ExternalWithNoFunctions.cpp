

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "some/path/Bar.h"

void register_ExternalWithNoFunctions(py::module_& module) {
    py::class_<::some::path::Bar, std::shared_ptr<::some::path::Bar>>(module, "ExternalWithNoFunctions")
        ;
}

