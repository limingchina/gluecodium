

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ListenerInterface.h"
#include "smoke/Weakling.h"
#include "memory"

void register_Weakling(py::module_& module) {
    py::class_<Weakling, std::shared_ptr<Weakling>>(module, "Weakling")
        .def_property("listener", &Weakling::get_listener)
        ;
}

