

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/StructsInstance.h"

void register_StructsInstance(py::module_& module) {
    py::class_<StructsInstance>(module, "StructsInstance")
        ;
}

