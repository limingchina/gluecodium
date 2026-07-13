

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SomeTypeCollection.h"
#include "smoke/UseTcException.h"

void register_UseTcException(py::module_& module) {
    py::class_<UseTcException>(module, "UseTcException")
        .def("do_nothing", &UseTcException::do_nothing)
        ;
}

