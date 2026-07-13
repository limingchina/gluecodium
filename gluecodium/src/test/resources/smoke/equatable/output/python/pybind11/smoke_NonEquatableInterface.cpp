

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/NonEquatableInterface.h"

void register_NonEquatableInterface(py::module_& module) {
    py::class_<NonEquatableInterface, std::shared_ptr<NonEquatableInterface>>(module, "NonEquatableInterface")
        ;
}

