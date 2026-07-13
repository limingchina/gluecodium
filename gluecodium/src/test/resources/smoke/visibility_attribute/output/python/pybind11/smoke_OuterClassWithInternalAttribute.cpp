

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/OuterClassWithInternalAttribute.h"
#include "cstdint"
#include "functional"

void register_OuterClassWithInternalAttribute(py::module_& module) {
    py::class_<OuterClassWithInternalAttribute>(module, "OuterClassWithInternalAttribute")
        ;
}

