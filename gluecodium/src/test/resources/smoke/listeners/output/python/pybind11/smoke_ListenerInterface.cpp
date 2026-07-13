

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ListenerInterface.h"

void register_ListenerInterface(py::module_& module) {
    py::class_<ListenerInterface, std::shared_ptr<ListenerInterface>>(module, "ListenerInterface")
        .def("notify", &ListenerInterface::notify)
        ;
}

