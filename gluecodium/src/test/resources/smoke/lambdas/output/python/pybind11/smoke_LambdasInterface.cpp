

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/LambdasInterface.h"
#include "cstdint"
#include "functional"
#include "memory"
#include "optional"
#include "vector"

void register_LambdasInterface(py::module_& module) {
    py::class_<LambdasInterface, std::shared_ptr<LambdasInterface>>(module, "LambdasInterface")
        .def("take_screenshot", &LambdasInterface::take_screenshot, py::arg("callback"))
        ;
}

