

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ExposeInternalInterface.h"

void register_ExposeInternalInterface(py::module_& module) {
    py::class_<ExposeInternalInterface, std::shared_ptr<ExposeInternalInterface>>(module, "ExposeInternalInterface")
        ;
}

