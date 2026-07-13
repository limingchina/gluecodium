

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/OverloadsWithComments.h"
#include "string"

void register_OverloadsWithComments(py::module_& module) {
    py::class_<OverloadsWithComments>(module, "OverloadsWithComments")
        .def("do_stuff", &OverloadsWithComments::do_stuff)
        .def("do_stuff", &OverloadsWithComments::do_stuff, py::arg("stuff"))
        ;
}

