

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/InterfaceWithLambda.h"
#include "functional"

void register_InterfaceWithLambda(py::module_& module) {
    py::class_<InterfaceWithLambda, std::shared_ptr<InterfaceWithLambda>>(module, "InterfaceWithLambda")
        ;
}

