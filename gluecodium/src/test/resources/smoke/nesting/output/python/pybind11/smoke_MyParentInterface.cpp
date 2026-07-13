

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/MyParentInterface.h"

void register_MyParentInterface(py::module_& module) {
    py::class_<MyParentInterface, std::shared_ptr<MyParentInterface>>(module, "MyParentInterface")
        ;
}

