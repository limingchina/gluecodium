

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/InternalClass.h"

void register_InternalClass(py::module_& module) {
    py::class_<InternalClass>(module, "InternalClass")
        .def("foo_bar", &InternalClass::foo_bar)
        ;
}

