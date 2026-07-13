

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/InterfaceInInterface.h"
#include "functional"
#include "memory"

void register_InterfaceInInterface(py::module_& module) {
    py::class_<InterfaceInInterface, std::shared_ptr<InterfaceInInterface>>(module, "InterfaceInInterface")
        ;
}

