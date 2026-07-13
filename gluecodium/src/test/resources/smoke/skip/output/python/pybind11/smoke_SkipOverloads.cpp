

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkipOverloads.h"

void register_SkipOverloads(py::module_& module) {
    py::class_<SkipOverloads>(module, "SkipOverloads")
        .def_readwrite("dummy", &SkipOverloads::dummy)
        .def("do_foo", &SkipOverloads::do_foo, py::arg("input"))
        ;
}

