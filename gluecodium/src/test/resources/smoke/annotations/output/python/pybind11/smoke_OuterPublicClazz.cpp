

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/OuterPublicClazz.h"

void register_OuterPublicClazz(py::module_& module) {
    py::class_<OuterPublicClazz>(module, "OuterPublicClazz")
        ;
}

