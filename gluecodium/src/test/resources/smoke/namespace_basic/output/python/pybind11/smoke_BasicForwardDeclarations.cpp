

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "root/space/smoke/Basic.h"
#include "root/space/smoke/BasicForwardDeclarations.h"
#include "memory"

void register_BasicForwardDeclarations(py::module_& module) {
    py::class_<BasicForwardDeclarations>(module, "BasicForwardDeclarations")
        .def("use_basic", &BasicForwardDeclarations::use_basic)
        ;
}

