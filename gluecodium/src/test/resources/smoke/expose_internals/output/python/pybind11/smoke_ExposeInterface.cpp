

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ExposeInterface.h"

void register_ExposeInterface(py::module_& module) {
    py::class_<ExposeInterface, std::shared_ptr<ExposeInterface>>(module, "ExposeInterface")
        ;
}

