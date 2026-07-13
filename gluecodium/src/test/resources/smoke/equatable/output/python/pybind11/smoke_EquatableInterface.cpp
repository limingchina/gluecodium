

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EquatableInterface.h"

void register_EquatableInterface(py::module_& module) {
    py::class_<EquatableInterface, std::shared_ptr<EquatableInterface>>(module, "EquatableInterface")
        ;
}

