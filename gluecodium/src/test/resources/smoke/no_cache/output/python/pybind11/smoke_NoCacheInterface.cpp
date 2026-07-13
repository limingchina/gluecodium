

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/NoCacheInterface.h"

void register_NoCacheInterface(py::module_& module) {
    py::class_<NoCacheInterface, std::shared_ptr<NoCacheInterface>>(module, "NoCacheInterface")
        .def("foo", &NoCacheInterface::foo)
        ;
}

