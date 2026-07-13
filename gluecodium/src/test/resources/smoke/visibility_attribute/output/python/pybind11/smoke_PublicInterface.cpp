

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/PublicClass.h"
#include "smoke/PublicInterface.h"

void register_PublicInterface(py::module_& module) {
    py::class_<PublicInterface, std::shared_ptr<PublicInterface>>(module, "PublicInterface")
        ;
}

