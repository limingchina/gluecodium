

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/OuterName.h"
#include "smoke/UseInnerName.h"

void register_UseInnerName(py::module_& module) {
    py::class_<UseInnerName>(module, "UseInnerName")
        .def("do_foo", &UseInnerName::do_foo)
        ;
}

