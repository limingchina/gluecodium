

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/forward/InnerClassForwardDeclarations.h"
#include "memory"

void register_InnerClassForwardDeclarations(py::module_& module) {
    py::class_<InnerClassForwardDeclarations>(module, "InnerClassForwardDeclarations")
        ;
}

