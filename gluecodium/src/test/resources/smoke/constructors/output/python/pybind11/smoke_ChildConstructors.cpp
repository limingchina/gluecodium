

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ChildConstructors.h"
#include "smoke/Constructors.h"
#include "memory"

void register_ChildConstructors(py::module_& module) {
    py::class_<ChildConstructors>(module, "ChildConstructors")
        .def("create", &ChildConstructors::create)
        .def("create", &ChildConstructors::create, py::arg("other"))
        ;
}

