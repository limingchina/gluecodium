

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/OuterStructWithInternalAttribute.h"
#include "cstdint"
#include "functional"

void register_OuterStructWithInternalAttribute(py::module_& module) {
    py::class_<OuterStructWithInternalAttribute>(module, "OuterStructWithInternalAttribute")
        .def_readwrite("inner", &OuterStructWithInternalAttribute::inner)
        ;
}

