

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/AsyncRenamed.h"

void register_AsyncRenamed(py::module_& module) {
    py::class_<AsyncRenamed>(module, "AsyncRenamed")
        .def("dispose", &AsyncRenamed::callDispose)
        ;
}

