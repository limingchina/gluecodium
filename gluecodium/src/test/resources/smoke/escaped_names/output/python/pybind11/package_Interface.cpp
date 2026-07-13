

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "package/Interface.h"

void register_Interface(py::module_& module) {
    py::class_<Interface, std::shared_ptr<Interface>>(module, "Interface")
        ;
}

