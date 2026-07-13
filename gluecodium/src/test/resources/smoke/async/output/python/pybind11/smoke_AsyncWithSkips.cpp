

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/AsyncWithSkips.h"
#include "string"

void register_AsyncWithSkips(py::module_& module) {
    py::class_<AsyncWithSkips>(module, "AsyncWithSkips")
        .def("make_shared_instance", &AsyncWithSkips::make_shared_instance, py::arg("android_context"))
        .def("make_shared_instance", &AsyncWithSkips::make_shared_instance)
        ;
}

