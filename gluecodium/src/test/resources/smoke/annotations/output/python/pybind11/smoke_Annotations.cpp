

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/Annotations.h"
#include "memory"
#include "optional"

void register_Annotations(py::module_& module) {
    py::class_<Annotations>(module, "Annotations")
        .def("test_optional", &Annotations::test_optional, py::arg("self"))
        ;
}

