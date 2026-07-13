

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/PlatformInternalInterface.h"

void register_PlatformInternalInterface(py::module_& module) {
    py::class_<PlatformInternalInterface, std::shared_ptr<PlatformInternalInterface>>(module, "PlatformInternalInterface")
        ;
}

