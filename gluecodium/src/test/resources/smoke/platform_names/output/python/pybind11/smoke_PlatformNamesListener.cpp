

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/fooListener.h"
#include "string"

void register_PlatformNamesListener(py::module_& module) {
    py::class_<fooListener, std::shared_ptr<fooListener>>(module, "PlatformNamesListener")
        .def("basic_method", &fooListener::FooMethod, py::arg("basic_parameter"))
        ;
}

